# excel格式（高级）

> 来源: https://www.datable.cn/docs/manual/exceladvanced

  * [](/)
  * [使用指南](../basic/使用指南.md)
  * excel格式（高级）

版本：4.x

本页总览

# excel格式（高级）

## 示例中用到的结构​

以下是示例中要用于的bean类型定义。
    
    
      
    <bean name="Type1">  
      <var name="a" type="int"/>  
      <var name="b" type="string"/>  
      <var name="c" type="bool"/>  
    </bean>  
      
    <bean name="Type2">  
      <var name="a" type="int"/>  
      <var name="b" type="bool"/>  
      <var name="c" type="Type1"/>  
    </bean>  
      
    <bean name="Vec3" sep=",">  
      <var name="x" type="float"/>  
      <var name="y" type="float"/>  
      <var name="z" type="float"/>  
    </bean>  
      
    <bean name="Type3">  
      <var name="a" type="int"/>  
      <var name="b" type="bool"/>  
      <var name="c" type="Type1#sep=,"/>  
    </bean>  
      
    <bean name="Type4">  
      <var name="a" type="string"/>  
      <var name="c" type="Vec3"/>  
    </bean>  
      
    <bean name="Title0">  
      <var name="a" type="int"/>  
      <var name="b" type="bool"/>  
      <var name="c" type="Title1"/>  
    </bean>  
      
    <bean name="Title1">  
      <var name="a" type="int"/>  
      <var name="b" type="string"/>  
      <var name="c" type="Title2"/>  
    </bean>  
      
    <bean name="Title2">  
      <var name="a" type="int"/>  
      <var name="b" type="int"/>  
    </bean>  
      
    

## 常量别名​

策划填写数据的时候，有时候希望用一个字符串来代表某个整数以方便阅读，同时也不容易出错。

在xml schema文件中定义`constalias`常量别名，在填写数据时使用它。

注意！常量别名仅能用于`byte、short、int、long、float、double`类型的数据，并且仅在excel族(xls、xlsx、csv等)、lite类型源数据类型中生效。

常量别名没有命名空间的概念，**不受module名影响** 。
    
    
    <mdoule name="test">  
      
      <constalias name="ITEM0" value="1001"/>  
      <constalias name="ITEM1" value="1002"/>  
      <constalias name="FLOAT1" value="1.5"/>  
      <constalias name="FLOAT2" value="2.5"/>  
      
    </module>  
    

![constalias](data:image/jpeg;base64,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)

## 限定列格式​

通过标题行及多级标题行，可以精确限定某个数据在某些列范围内。

对于只有一个原子值的简单类型数据，限定列格式下，由于能够非常清晰知道它的值必然来自某一单元格，所以它支持**默认值** 语义，即如果单元格为空，值取默认值，例如 int类型默认值为0，int?默认值为null。

限定列格式下，多态bean类型需要用 $type 列来指定具体类型名，可空bean类型也需要用$type列来指示是有效bean还是空bean。

如果最低层的限定列的类型为容器或者bean，由于限定列只限定了该数据整体范围，但**未限定** 子数据的范围，因此读取子数据的格式为**流式格式** ，即按顺序读入每个子数据。

![titlelimit](/assets/images/titlelimit-602bb9196f754dd4a3c55d766a6d301c.jpg)

### `flags=1` 的 enum 类型支持列限定模式。​

用枚举项作为列名，最终值为所有非0或空的枚举项的**或值** 。

![titlle_enum](/assets/images/title_enum-5c96663bfbbb1992cd6e2713cec78d1b.jpg)

### 多态bean支持 $type与$value 分别配置的列限定或流式格式的混合填写方式​

即用$type列为限定类型，用$value列来限定bean的实际字段，并且$value中以流式填写bean的所有字段。

![title_dynamic_bean](/assets/images/title_dynamic_bean-482422aabcccdac7d7fbd6d369cdbe4c.jpg)

### map的列限定格式​

有两种填法：

  * 多行填法。此时要求 `$key`子列对应key字段，剩余列对应value的子字段。如下图y1字段所示
  * 非多行填法。可以将key作为子字段名，如果对应的单元不为空，则对应key-value的键值对存在。例如下图中id=1的记录， 它的y2字段最终值为`{{"aaa", 1}, {"ccc":2}}`；id=2的记录，它的y2字段最终值为`{{"bbb", 10}, {"ccc", 20}, {"ddd", 30}}`。 如下图y2字段所示



![title_map](/assets/images/title_map-13d12e479c22398dc7b73af7e44c3232.jpg)

提示

以上仅是map的列限定格式下的填法。map还有额外两种流式格式下的填法。

## 多级标题头​

有时候，某些字段是复合结构，如bean或者结构列表之类的类型，按顺序填写时，由于流式格式中空白单元格会被自动跳过， 导致实践中容易写错。另外，流式格式不支持空白单元格表示默认值，也无法直观地限定某个子字段在某一铺，带来一些不便。 多级标题可以用于限定bean或容器的子字段，提高了可读性，避免流式格式的意外错误。

通过在某个`##var`行下新增一行`##var`，为添加子字段名，则可以为子字段设置标题头。可以有任意级别的子标题头。 下图中，x1只有1级子标题头，y1有2级，y2只有1级，z1有3级。

![colloumlimit](/assets/images/multileveltitle-3e1e45452ed00a0da5f65d40f557e62c.jpg)

## 多行结构列表​

有时候列表结构的每个结构字段较多，如果水平展开则占据太多列，不方便编辑，如果拆表，无论程序还是策划都不方便，此时可以使用多行模式。

将字段名标记为`*<name>`即可表达要将这个数据多行读入。支持任意层次的多行结构列表（也即多行结构中的每个元素也可以是多行）。 对于`array,bean`、`list,bean`这样的结构容器类型，还可以配合限定列格式，限定元素中每个子字段的列，如字段x2所示。

![map](/assets/images/multiline-d4bd4a85c32fa4b9978c22cd9d0adaa9.jpg)

## 紧凑格式​

如果某个数据是非原子数据（如bean或容器），并且它被限定到某些单元格列范围或者是sep分割的数据的一部分，则它的解析方式为**紧凑格式** 。

![image](/assets/images/compact-6388075acdb892d9a2987e3fe87e6485.jpg)

由于紧凑格式比较复杂，单独用一篇文档介绍它。详细见[Excel紧凑格式](Excel 紧凑格式.md)。

## 数据标签过滤​

开发期经常会制作一些仅供开发使用的配置，比如测试道具，比如自动化测试使用的配置，开发者希望在正式发布时不导出这些数据。 可以通过给记录加上tag，再配合命令行参数 --excludeTag实现这个目的 。`##`是一个特殊的tag，表示这个数据被永久注释，任何情况下都不会被导出。 详细文档请阅读 [数据 tag](数据tag.md)。

如下图，id=3和id=4的记录，在命令行添加 `--excludeTag dev` 参数后，导出时不会包含这两个dev记录。

![tag](/assets/images/tag-e58c3cc27b698633de18a8f060eb96a3.jpg)

