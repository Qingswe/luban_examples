# Excel Format (Advanced)

> 来源: https://www.datable.cn/en/docs/manual/exceladvanced

  * [](/en/)
  * [User Guide](../basic/User Guide.md)
  * Excel Format (Advanced)

Version: 4.x

On this page

# Excel Format (Advanced)

## Structure used in the example​

The following is the bean type definition to be used in the example.
    
    
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
    

## Constant alias​

When planning to fill in data, sometimes you want to use a string to represent an integer for easy reading and less error-prone.

Define the `constalias` constant alias in the xml schema file and use it when filling in data.

Note! Constant aliases can only be used for data of the `byte, short, int, long, float, double` type, and are only effective in the excel family (xls, xlsx, csv, etc.) and lite type source data types.

Constant aliases have no concept of namespace and are **not affected by module names**.
    
    
    <mdoule name="test">   
        <constalias name="ITEM0" value="1001"/>   
        <constalias name="ITEM1" value="1002"/>   
        <constalias name="FLOAT1" value="1.5"/>   
        <constalias name="FLOAT2" value="2.5"/>  
    </module>  
    

![constalias](data:image/jpeg;base64,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)

## Limit column format​

Using the title row and multi-level title row, you can accurately limit a certain data to a certain column range.

For simple type data with only one atomic value, in the qualified column format, since it is very clear that its value must come from a certain cell, it supports **default value** semantics, that is, if the cell is empty, the value takes the default value, for example, the default value of int type is 0, and the default value of int? is null.

In the qualified column format, polymorphic bean types need to use the $type column to specify the specific type name, and nullable bean types also need to use the $type column to indicate whether it is a valid bean or an empty bean.

If the lowest level qualified column type is container or bean, since the qualified column only limits the overall range of the data, but **does not limit** the range of sub-data, the format for reading sub-data is **streaming format** , that is, each sub-data is read in sequence.

![titlelimit](/en/assets/images/titlelimit-602bb9196f754dd4a3c55d766a6d301c.jpg)

### `flags=1` enum type supports column qualification mode.​

Use enumeration items as column names, and the final value is **or value** of all non-0 or empty enumeration items.

![titlle_enum](/en/assets/images/title_enum-5c96663bfbbb1992cd6e2713cec78d1b.jpg)

### Polymorphic beans support a mixed filling method of $type and $value configured separately, column restriction or stream format​

That is, use the $type column as the restriction type, use the $value column to restrict the actual field of the bean, and fill all the fields of the bean in $value in a stream format.

![title_dynamic_bean](/en/assets/images/title_dynamic_bean-482422aabcccdac7d7fbd6d369cdbe4c.jpg)

### Map column restriction format​

There are two filling methods:

  * Multi-line filling method. In this case, the `$key` sub-column is required to correspond to the key field, and the remaining columns correspond to the sub-fields of the value. As shown in the y1 field in the figure below

  * Non-multi-line filling method. The key can be used as the sub-field name. If the corresponding cell is not empty, the corresponding key-value pair exists. For example, in the following figure, the record with id=1, its y2 field has a final value of `{{"aaa", 1}, {"ccc":2}}`; the record with id=2 has a final value of `{{"bbb", 10}, {"ccc", 20}, {"ddd", 30}}`. As shown in the y2 field in the following figure




![title_map](/en/assets/images/title_map-13d12e479c22398dc7b73af7e44c3232.jpg)

tip

The above is only the filling method under the column-limited format of map. There are two additional filling methods under the flow format of map.

## Multi-level title header​

Sometimes, some fields are composite structures, such as beans or structure lists. When filling in order, blank cells will be automatically skipped in the flow format, which makes it easy to write errors in practice. In addition, the flow format does not support blank cells to represent default values, and it is also impossible to intuitively limit a subfield to a certain store, which brings some inconvenience. Multi-level titles can be used to limit the sub-fields of beans or containers, which improves readability and avoids unexpected errors in streaming formats.

By adding a new line `##var` under a `##var` line, you can set a title for the sub-field to add a sub-field name. There can be any level of sub-title headers.

In the figure below, x1 has only 1 level of sub-title headers, y1 has 2 levels, y2 has only 1 level, and z1 has 3 levels.

![colloumlimit](/en/assets/images/multileveltitle-3e1e45452ed00a0da5f65d40f557e62c.jpg)

## Multi-line structure list​

Sometimes each structure field of the list structure is too many. If it is expanded horizontally, it will occupy too many columns and is not convenient for editing. If the table is split, it will be inconvenient for both programming and planning. In this case, you can use multi-line mode.

Marking the field name as `*<name>` can express that you want to read this data in multiple lines. Supports multi-line structure lists of any level (that is, each element in the multi-line structure can also be multiple lines). For structural container types such as `array,bean` and `list,bean`, you can also use the limited column format to limit the columns of each subfield in the element, as shown in field x2.

![map](/en/assets/images/multiline-d4bd4a85c32fa4b9978c22cd9d0adaa9.jpg)

## Compact format​

If a data is non-atomic data (such as bean or container), and it is limited to a certain cell column range or part of the data separated by sep, its parsing method is **compact format**.

![image](/en/assets/images/compact-6388075acdb892d9a2987e3fe87e6485.jpg)

Because the compact format is relatively complex, it is introduced in a separate document. For details, see [Excel compact format](Excel compact format.md).

## Data tag filtering​

During the development period, some configurations that are only used for development are often made, such as test props, such as configurations used for automated testing. Developers hope not to export these data when they are officially released. This can be achieved by adding tags to the records and then using the command line parameter --excludeTag. `##` is a special tag, which means that this data is permanently annotated and will not be exported under any circumstances. For detailed documentation, please read [data tag](data tag.md).

As shown in the figure below, after adding the `--excludeTag dev` parameter in the command line, the two dev records of id=3 and id=4 will not be included in the export.

![tag](/en/assets/images/tag-e58c3cc27b698633de18a8f060eb96a3.jpg)

