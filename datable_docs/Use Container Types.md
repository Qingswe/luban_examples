# Use Container Types

> 来源: https://www.datable.cn/en/docs/beginner/usecollection

  * [](/en/)
  * [The tutorial](/en/docs/beginner)
  * Use Container Types

Version: 4.x

On this page

# Use Container Types

Containers are also the most commonly used types. Luban supports a variety of container data formats, and you can choose the most suitable type and fill it out according to your needs.

For detailed definition documents, see [schema logical structure](/en/docs/manual/schema) and [type system](/en/docs/manual/types), and for detailed data documents, see [Excel format (primary)](/en/docs/manual/excel) and [Excel format (advanced)](/en/docs/manual/exceladvanced).

## Container definition​

Currently supports 4 basic container types, see [Container Type](../manual/types#Container Type) for details:

Container Type| Description| Example  
---|---|---  
array| Array type, similar to list, but the generated code corresponds to the native array type, such as `xxx[]` in C# language| `array,int`, `array,string`, `array,Color`, `array,Item`  
list| List type, similar to array, but the generated code corresponds to the List container type, such as `List<xx>` in C# language| `list,int`, `list,string`, `list,Color`, `list,Item`  
set| Set type, requires unique element values, the generated code corresponds to the Set container type, such as `HashSet<xx>` in C# language| `set,int`、`set,string`、`set,Color`  
map| Dictionary type, key is required to be unique, the generated code corresponds to Map type, such as `Dictionary<xx,yy>` in C# language| `map,int,int`、`map,string,string`, `map,Color,int`，`map,int,Item`  
  
## Fill in array, list, set data​

There are two common ways to fill in:

  * Occupy multiple cells, one element in each cell

  * Occupy one cell, each element is separated by a separator




When occupying multiple cells, the field name needs to occupy multiple columns. At this time, you need to merge cells to make the field occupy multiple columns. If you are using a file format such as csv that does not support merged cells, you can use `[{field name}` and `{field name}]` in the start and end columns to indicate that this field occupies multiple columns.

When occupying a cell, you need to use `sep=x` to specify the separator. The separator can be common characters such as ',', '|', ';', '&', '_', '-', such as `sep=,`.

![item](/en/assets/images/use_list-9c0c728dc4e403625f1b62c04dd9d651.jpg)

The element type can also be an enumeration or structure type. The figure below only shows the array. The filling method of list and set types is similar.

![item](/en/assets/images/use_list2-825e82024dedf61964386e2f433ec1eb.jpg)

You can even fill in multiple lines. As long as '*' is added before the field name, it means filling in multiple lines of data, one element per line. For details, see [Excel Format (Advanced)](/en/docs/manual/exceladvanced).

![item](/en/assets/images/use_list3-8b7ed9a5f3ed0834204c44af6d6d0e5b.jpg)

## Fill in map data​

The dictionary type contains key and value, so it is more complicated than array and the like.

Similarly, map can also be filled in a cell. In order to better distinguish key and value, and to divide each key-value pair, generally map's sep will be filled in 2. The example is as follows:

![item](/en/assets/images/use_map-fa7e9e195425fd8511b92dfea680beab.jpg)

The value type of map can also be a structure type, similar to this:

![item](/en/assets/images/use_map2-bce4de0106a053c50478ccb3a730bb27.jpg)

map can also be filled in multiple lines, as follows:

![item](/en/assets/images/use_map3-bf848e769a2351bcc5171426e4aba165.jpg)

