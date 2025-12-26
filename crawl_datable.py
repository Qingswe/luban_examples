#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爬取 www.datable.cn 的所有文章并保存为 Markdown 文件
"""

import os
import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import html2text

class DatableCrawler:
    def __init__(self, base_url='https://www.datable.cn/docs/', output_dir='datable_docs'):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls = set()
        self.failed_urls = []  # 记录失败的URL
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0  # 不限制行宽
        
    def sanitize_filename(self, filename):
        """清理文件名，移除非法字符"""
        # 移除或替换非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        # 限制文件名长度
        if len(filename) > 200:
            filename = filename[:200]
        return filename or 'untitled'
    
    def get_page_content(self, url, retries=3):
        """获取页面内容"""
        for attempt in range(retries):
            try:
                print(f"正在获取: {url} (尝试 {attempt + 1}/{retries})")
                response = self.session.get(url, timeout=60)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
            except Exception as e:
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"获取失败，{wait_time}秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"获取页面失败 {url}: {e}")
                    return None
        return None
    
    def extract_article_content(self, soup, url):
        """提取文章内容"""
        # 尝试多种可能的内容选择器
        content_selectors = [
            {'tag': 'article'},
            {'tag': 'main'},
            {'class': 'content'},
            {'class': 'article-content'},
            {'class': 'markdown-body'},
            {'id': 'content'},
            {'id': 'article'},
        ]
        
        content = None
        for selector in content_selectors:
            if 'tag' in selector:
                content = soup.find(selector['tag'])
            elif 'class' in selector:
                content = soup.find(class_=selector['class'])
            elif 'id' in selector:
                content = soup.find(id=selector['id'])
            
            if content:
                break
        
        # 如果找不到特定容器，尝试获取 body 内容
        if not content:
            content = soup.find('body')
        
        return content
    
    def extract_title(self, soup):
        """提取文章标题"""
        # 尝试多种标题选择器
        title_selectors = [
            soup.find('h1'),
            soup.find('title'),
            soup.find('meta', property='og:title'),
        ]
        
        for title_elem in title_selectors:
            if title_elem:
                if title_elem.name == 'meta':
                    return title_elem.get('content', '').strip()
                return title_elem.get_text().strip()
        
        return 'Untitled'
    
    def find_all_article_links(self, soup, base_url):
        """查找所有文章链接"""
        links = set()
        
        # 如果 base_url 是 /docs/，则爬取所有 /docs/ 下的链接
        # 否则只爬取指定子目录的链接
        if self.base_url.rstrip('/').endswith('/docs'):
            # 爬取整个 docs 目录
            target_path = '/docs/'
        else:
            # 提取目标路径（如 /docs/basic 或 /docs/beginner）
            target_path = '/docs/' + self.base_url.split('/docs/')[-1] if '/docs/' in self.base_url else ''
        
        # 对于 basic 目录，也需要爬取 manual 目录下的链接
        target_paths = [target_path]
        if '/docs/basic' in self.base_url:
            target_paths.append('/docs/manual')
        
        # 查找所有链接
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            
            # 检查是否属于目标路径
            is_target_link = False
            for path in target_paths:
                if path and (path in full_url or path in href):
                    is_target_link = True
                    break
            
            if is_target_link:
                # 移除锚点
                parsed = urlparse(full_url)
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                # 只添加有效的文档页面（排除首页和外部链接）
                if parsed.path and parsed.path != '/' and 'datable.cn' in parsed.netloc:
                    # 确保是 /docs/ 下的链接
                    if '/docs/' in parsed.path:
                        links.add(clean_url)
        
        return links
    
    def save_as_markdown(self, title, content, url):
        """保存为 Markdown 文件"""
        if not content:
            print(f"警告: {url} 没有找到内容")
            return False
        
        # 转换为 Markdown
        markdown_content = self.html_converter.handle(str(content))
        
        # 构建完整的 Markdown 文档
        full_markdown = f"""# {title}

> 来源: {url}

{markdown_content}
"""
        
        # 保存文件
        filename = self.sanitize_filename(title) + '.md'
        filepath = self.output_dir / filename
        
        # 如果文件已存在，添加序号
        counter = 1
        while filepath.exists():
            filename = f"{self.sanitize_filename(title)}_{counter}.md"
            filepath = self.output_dir / filename
            counter += 1
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_markdown)
            print(f"[成功] 已保存: {filepath}")
            return True
        except Exception as e:
            print(f"[失败] 保存失败 {filepath}: {e}")
            return False
    
    def crawl(self):
        """开始爬取"""
        print(f"开始爬取: {self.base_url}")
        print(f"输出目录: {self.output_dir.absolute()}")
        
        # 待处理的 URL 队列
        # 如果 base_url 是 /docs/，从多个入口页面开始
        if self.base_url.rstrip('/').endswith('/docs'):
            urls_to_process = [
                'https://www.datable.cn/docs/beginner',
                'https://www.datable.cn/docs/basic',
            ]
        else:
            urls_to_process = [self.base_url]
        
        while urls_to_process:
            current_url = urls_to_process.pop(0)
            
            # 跳过已访问的 URL
            if current_url in self.visited_urls:
                continue
            
            self.visited_urls.add(current_url)
            
            # 获取页面内容
            html_content = self.get_page_content(current_url)
            if not html_content:
                self.failed_urls.append(current_url)
                continue
            
            # 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 提取标题和内容
            title = self.extract_title(soup)
            content = self.extract_article_content(soup, current_url)
            
            # 保存为 Markdown
            if content:
                self.save_as_markdown(title, content, current_url)
            
            # 查找所有相关链接
            article_links = self.find_all_article_links(soup, current_url)
            for link in article_links:
                if link not in self.visited_urls and link not in urls_to_process:
                    urls_to_process.append(link)
            
            # 避免请求过快
            time.sleep(1)
        
        print(f"\n爬取完成！共处理 {len(self.visited_urls)} 个页面")
        print(f"文件保存在: {self.output_dir.absolute()}")
        
        if self.failed_urls:
            print(f"\n失败的URL ({len(self.failed_urls)} 个):")
            for url in self.failed_urls:
                print(f"  - {url}")
            print("\n可以稍后重试这些URL")
    
    def retry_failed_urls(self, failed_urls):
        """重试失败的URL"""
        print(f"\n开始重试 {len(failed_urls)} 个失败的URL...")
        for url in failed_urls:
            if url not in self.visited_urls or True:  # 即使访问过也重试
                html_content = self.get_page_content(url)
                if html_content:
                    soup = BeautifulSoup(html_content, 'html.parser')
                    title = self.extract_title(soup)
                    content = self.extract_article_content(soup, url)
                    if content:
                        self.save_as_markdown(title, content, url)
                        self.visited_urls.add(url)
                time.sleep(2)  # 重试时增加延迟

if __name__ == '__main__':
    # 支持命令行参数
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
        # 根据URL自动生成输出目录名
        url_part = base_url.split('/docs/')[-1] if '/docs/' in base_url else 'docs'
        if not url_part or url_part == '':
            output_dir = 'datable_docs_all'
        else:
            output_dir = f'datable_docs_{url_part.replace("/", "_")}'
        crawler = DatableCrawler(base_url=base_url, output_dir=output_dir)
    else:
        # 默认爬取整个 docs 目录
        crawler = DatableCrawler(base_url='https://www.datable.cn/docs/', output_dir='datable_docs_all')
    crawler.crawl()

