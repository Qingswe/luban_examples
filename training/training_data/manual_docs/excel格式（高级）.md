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
    

| ## | id | x1 | x2 | x3 | x4 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| | 1 | ITEM0 | ITEM0 | FLOAT1 | FLOAT2 |
| | 2 | ITEM1 | ITEM1 | FLOAT1 | FLOAT2 |
| | 3 | 1 | 2 | 1 | 2 |

## 限定列格式​

通过标题行及多级标题行，可以精确限定某个数据在某些列范围内。

对于只有一个原子值的简单类型数据，限定列格式下，由于能够非常清晰知道它的值必然来自某一单元格，所以它支持**默认值** 语义，即如果单元格为空，值取默认值，例如 int类型默认值为0，int?默认值为null。

限定列格式下，多态bean类型需要用 $type 列来指定具体类型名，可空bean类型也需要用$type列来指示是有效bean还是空bean。

如果最低层的限定列的类型为容器或者bean，由于限定列只限定了该数据整体范围，但**未限定** 子数据的范围，因此读取子数据的格式为**流式格式** ，即按顺序读入每个子数据。

| ##var | id | x1 | x1 | y1 | y1 | y1 | a1 | a1 | a1 | a1 | x2 | x2 | x2 | a2 | a2 | a2 | a2 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| ##type | int | Title2 | Title2 | Title1 | Title1 | Title1 | Shape | Shape | Shape | Shape | Title2? | Title2? | Title2? | Shape? | Shape? | Shape? | Shape? |
| ##var | | a | b | a | b | c | $type | radius | width | height | $type | a | b | $type | radius | width | height |
| ##var | | | | a | b | | | | | | | | | | | | |
| ##var | | | | | | | | | | | | | | | | | |
| | 1 | 10 | 20 | 10 abc | 11 | 22 | Circle | 100 | | | {} | 10 | 20 | Circle | 100 | | |
| | 2 | | | 11 | | | Rectangle | | 10 | 20 | null | | | Rectangle | | 10 | 20 |
| | 3 | | | 12 | | | 圆 | 200 | | | {} | 20 | 30 | 圆 | 200 | | |
| | 4 | | | 13 abc | 14 | 25 | 矩形 | 100 | 200 | | {} | 30 | 40 | null | | | |

### `flags=1` 的 enum 类型支持列限定模式。​

用枚举项作为列名，最终值为所有非0或空的枚举项的**或值** 。

| ##var | id | x3 | x3 | x3 | x3 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| ##type | int | AccessFlag | AccessFlag | AccessFlag | AccessFlag |
| ##var | | READ | WRITE | APPEND | TRUNCT |
| ##group | | | | | |
| ## | id | | | | |
| | 1001 | 1 | | 1 | |
| | 1002 | | 1 | | 1 |
| | 1003 | 1 | | | |
| | 1004 | | 1 | | |
| | 1005 | 1 | 1 | 1 | 1 |
| | 1006 | | | | |
| | 1007 | 1 | | | |

### 多态bean支持 $type与$value 分别配置的列限定或流式格式的混合填写方式​

即用$type列为限定类型，用$value列来限定bean的实际字段，并且$value中以流式填写bean的所有字段。

| ##var | id | a1 | a1 | a1 |
| ---- | ---- | ---- | ---- | ---- |
| ##type | int | Shape | Shape | Shape |
| ##var | | $type | $value | $value |
| | 1 | Circle | 100 | |
| | 2 | Rectangle | 10 | 20 |
| | 3 | 圆 | 200 | |
| | 4 | 矩形 | 100 | 200 |

### map的列限定格式​

有两种填法：

  * 多行填法。此时要求 `$key`子列对应key字段，剩余列对应value的子字段。如下图y1字段所示
  * 非多行填法。可以将key作为子字段名，如果对应的单元不为空，则对应key-value的键值对存在。例如下图中id=1的记录， 它的y2字段最终值为`{{"aaa", 1}, {"ccc":2}}`；id=2的记录，它的y2字段最终值为`{{"bbb", 10}, {"ccc", 20}, {"ddd", 30}}`。 如下图y2字段所示



| ## | id | *y1 | *y1 | *y1 | *y1 | y2 | y2 | y2 | y2 | y2 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| ##type | int | map,int,Type1 | map,int,Type1 | map,int,Type1 | map,int,Type1 | map,string,int | map,string,int | map,string,int | map,string,int | map,string,int |
| ##var | | $key | a | b | c | aaa | bbb | ccc | ddd | eee |
| | 1 | 1 | 10 aaa | TRUE | | 1 | | 2 | |
| | | 2 | 20 bbb | FALSE | | | | | | |
| | 2 | 1 | 100 abc | FALSE | | | 10 | 20 | 30 | |
| | | 3 | 300 hello | TRUE | | | | | | |
| | 3 | 3 | 30 ccc | TRUE | | 2 | | 38 | | |

提示

以上仅是map的列限定格式下的填法。map还有额外两种流式格式下的填法。

## 多级标题头​

有时候，某些字段是复合结构，如bean或者结构列表之类的类型，按顺序填写时，由于流式格式中空白单元格会被自动跳过， 导致实践中容易写错。另外，流式格式不支持空白单元格表示默认值，也无法直观地限定某个子字段在某一铺，带来一些不便。 多级标题可以用于限定bean或容器的子字段，提高了可读性，避免流式格式的意外错误。

通过在某个`##var`行下新增一行`##var`，为添加子字段名，则可以为子字段设置标题头。可以有任意级别的子标题头。 下图中，x1只有1级子标题头，y1有2级，y2只有1级，z1有3级。

| ##var | id | x1 | x1 | | y1 | y1 | y1 | y1 | y2 | y2 | y2 | y2 | z1 | z1 | z1 | z1 | z1 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| ##type | int | Title2 | Title2 | | Title1 | Title1 | Title1 | Title1 | Title1 | Title1 | Title1 | Title1 | Title0 | Title0 | Title0 | Title0 | Title0 |
| ##var | | a | b | | a | b | c | c | a | b | c | c | a | b | Title0 | c | c |
| ##var | | | | | | | a | b | | | a | b | | | a | a | b |
| ##var | | | | | | | | | | | | | | | | | |
| | 1 | 10 | 20 | | 10 abc | 11 | 22 | | 10 aaa | 11 | 22 | | 1 | TRUE | 2 aaa | 10 | 20 |
| | 2 | 11 | 21 | | 11 abc | 12 | 23 | | 11 aaa | 12 | 23 | | 2 | TRUE | 3 aaa | 11 | 21 |
| | 3 | 12 | 22 | | 12 abc | 13 | 24 | | 12 aaa | 13 | 24 | | 3 | TRUE | 4 aaa | 12 | 22 |
| | 4 | 13 | 23 | | 13 abc | 14 | 25 | | 13 aaa | 14 | 25 | | 4 | TRUE | 5 aaa | 13 | 23 |
| | 5 | 14 | 24 | | 14 abc | 15 | 26 | | 14 aaa | 15 | 26 | | 5 | TRUE | 6 aaa | 14 | 24 |

## 多行结构列表​

有时候列表结构的每个结构字段较多，如果水平展开则占据太多列，不方便编辑，如果拆表，无论程序还是策划都不方便，此时可以使用多行模式。

将字段名标记为`*<name>`即可表达要将这个数据多行读入。支持任意层次的多行结构列表（也即多行结构中的每个元素也可以是多行）。 对于`array,bean`、`list,bean`这样的结构容器类型，还可以配合限定列格式，限定元素中每个子字段的列，如字段x2所示。

| ## | id | *x1 | *x1 | *x1 | *x2 | *x2 | *x2 | *y1 | *y1 | *y1 | *y2 | *y2 | *y2 | *y2 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| ##type | int | list,Type1 | list,Type1 | list,Type1 | list,Type1 | list,Type1 | list,Type1 | map,int,Type1 | map,int,Type1 | map,int,Type1 | map,int,TestValue | map,int,TestValue | map,int,TestValue | map,int,TestValue |
| ##var |  |  |  |  | a | b | c |  |  |  | $key | a | b | c |
|  | 1 | 10 | aaa | TRUE | 10 | aaa | TRUE | 100 | 1 | aaa | TRUE | 1 | 1 | aaa | TRUE |
|  |  | 20 | bbb | FALSE | 20 | bbb | FALSE | 200 | 20 | bb | FALSE | 2 | 2 | aaa | TRUE |
|  |  |  |  |  | 30 | aaa |  |  |  |  |  |  |  |  |
|  | 2 | 10 | aaa | TRUE | 10 | aaa |  | 10 | 11 | abc | TRUE | 1 | 1 | aaa | TRUE |
|  |  | 20 | bbb |  |  |  |  |  |  |  |  | 3 | 3 | aaa | TRUE |
|  |  | 21 | bbb | FALSE |  |  |  |  |  |  |  | 4 | 4 | aaa | TRUE |

## 紧凑格式​

如果某个数据是非原子数据（如bean或容器），并且它被限定到某些单元格列范围或者是sep分割的数据的一部分，则它的解析方式为**紧凑格式** 。

| v31 | v32#format=json | v33#format=lua | v34#format=lite | v41 |
| ---- | ---- | ---- | ---- | ---- |
| vec3 | vec3 | vec3 | vec3 | (list# |
|  |  |  |  |  |
| 1,2,3 | {"x":1, "y":2, "z":3} | {x=1,y=2,z=3} | {1,2,3} | 1,2,3 |

由于紧凑格式比较复杂，单独用一篇文档介绍它。详细见[Excel紧凑格式](Excel 紧凑格式.md)。

## 数据标签过滤​

开发期经常会制作一些仅供开发使用的配置，比如测试道具，比如自动化测试使用的配置，开发者希望在正式发布时不导出这些数据。 可以通过给记录加上tag，再配合命令行参数 --excludeTag实现这个目的 。`##`是一个特殊的tag，表示这个数据被永久注释，任何情况下都不会被导出。 详细文档请阅读 [数据 tag](数据tag.md)。

如下图，id=3和id=4的记录，在命令行添加 `--excludeTag dev` 参数后，导出时不会包含这两个dev记录。

| ##var | id | a | b | c |
| ---- | ---- | ---- | ---- | ---- |
| ##type | int | long | string | string |
|  | 1 | 1 | aaa | 正式数据 |
| ## | 1 | 1 | bbb | 正式数据 |
| dev | 1 | 2 | aaa | 这是测试数据 |
| dev | 4 | 5 | aaa | 这是测试数据 |
|  | 5 | 6 | aaa | 正式数据 |
|  | 6 | 7 | aaa | 正式数据 |
|  | 7 | 8 | aaa | 正式数据 |
|  | 8 | 9 | aaa | 正式数据 |
