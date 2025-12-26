# introduce

> 来源: https://www.datable.cn/en/docs/intro

  * [](/en/)
  * Introduce

Version: 4.x

On this page

# introduce

![icon](/en/assets/images/logo-4bc800312bd07ef2f4d6e4568b9b5758.png)

[![license](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT) ![star](https://img.shields.io/github/stars/focus-creative-games/luban?style=flat-square)

luban is a powerful, easy-to-use, elegant, and stable game configuration solution. It is designed to meet the needs of simple to complex game configuration workflows from small to very large game projects.

luban can handle a variety of file types, supports mainstream languages, can generate multiple export formats, supports rich data inspection functions, has good cross-platform capabilities, and generates extremely fast. Luban has a clear and elegant generation pipeline design, supports good modularization and plug-in, and is convenient for developers to carry out secondary development. Developers can easily adapt luban to their own configuration format, and customize powerful configuration tools that meet project requirements.

Luban standardizes the game configuration development workflow, which can greatly improve the efficiency of planning and programming.

## Core features​

  * Rich source data format. Support excel family (csv, xls, xlsx, xlsm), json, xml, yaml, lua, etc.
  * Rich export formats. Support generating binary, json, bson, xml, lua, yaml and other format data
  * Enhanced excel format. Simple configurations such as simple lists, substructures, structured lists, and arbitrarily complex deep nested structures can be concisely configured
  * Complete type system. Not only can it express common specification line lists, but it can flexibly and elegantly express complex GamePlay data such as behavior trees, skills, plots, and dungeons because **supports OOP type inheritance**
  * Support multiple languages. Supports generating language codes such as c#, java, go, cpp, lua, python, typescript, etc.
  * Support mainstream message schemes. protobuf(schema + binary + json), flatbuffers(schema + json), msgpack(binary)
  * Powerful data verification capability. ref reference check, path resource path, range range check, etc.
  * Perfect localization support
  * Supports all major game engines and platforms. Support Unity, Unreal, Cocos, Godot, Laya, WeChat games, etc.
  * Good cross-platform capability. It can run well on Win, Linux, and Mac platforms.
  * Support all mainstream hot update solutions. hybridclr, ilruntime, {x,t,s}lua, puerts, etc.
  * Clear and elegant generation pipeline, it is easy to carry out secondary development on the basis of luban, and customize a configuration tool suitable for your own project style.



## Excel format overview​

basic data format

![primitive_type](/en/assets/images/primitive_type-d85cfb51a19f153b0fdf9ac299b4a5e1.jpg)

enum data format

![enum](/en/assets/images/enum-dee044226803effc6032313e7c4981e7.jpg)

bean data format

![bean](/en/assets/images/bean-85ba1ecb5030e30e47c4487ec0c261d2.jpg)

Polymorphic bean data format

![bean](/en/assets/images/bean2-04651442a9b2d1cb2c12f18f23cb9bcf.jpg)

container

![collection](/en/assets/images/collection-5416a057bd788208fb64a6b5420663ef.jpg)

nullable type

![nullable](/en/assets/images/nullable-8a3a3a221c9def07e16e04ccf86a9b84.jpg)

no primary key table

![table_list_not_key](/en/assets/images/table_list_not_key-082f29e3fc26a5cc33d982f34a4c1e60.jpg)

Multi-primary key table (joint index)

![table_list_union_key](/en/assets/images/table_list_union_key-27d9231b4a48f42aa5f79cf80e2ffd81.jpg)

Multi-primary key table (independent index)

![table_list_indep_key](/en/assets/images/table_list_indep_key-3d2f4e268f41d88d0312c350bdf075e4.jpg)

singleton table

Some configurations have only one copy globally, such as the opening level of the guild module, the initial size of the backpack, and the upper limit of the backpack. At this time, it is more appropriate to use a singleton table to configure these data.

![singleton](/en/assets/images/singleton2-b46d4b2c6cccbabd69296a59222fe9d4.jpg)

vertical table

Most tables are horizontal tables, that is, one record per row. Some tables, such as singleton tables, are more comfortable to fill in vertically, with one field per line. A1 is `##column` or `##vertical` means using vertical table mode. The singleton table above is filled in as follows in vertical table mode.

![singleton](/en/assets/images/singleton-9b7d41bf32c0c214d2baac6cbbd5cea8.jpg)

Use sep to read beans and nested beans.

![sep_bean](/en/assets/images/sep_bean-82bc281e78eff8ae7fb8e4b9c0110457.jpg)

Use sep to read normal containers.

![sep_bean](/en/assets/images/sep_container1-4a8bd3a370e5707614dae98f3fcf51e2.jpg)

Use sep to read structure containers.

![sep_bean](/en/assets/images/sep_container2-c8fa336d283b22df2d9e7b70742e8558.jpg)

multi-level header

![colloumlimit](/en/assets/images/multileveltitle-3e1e45452ed00a0da5f65d40f557e62c.jpg)

Qualify column format

![titlelimit](/en/assets/images/titlelimit-602bb9196f754dd4a3c55d766a6d301c.jpg)

Enumerated column-qualified format

![title_enum](/en/assets/images/title_enum-5c96663bfbbb1992cd6e2713cec78d1b.jpg)

polymorphic bean column qualification format

![title_dynamic_bean](/en/assets/images/title_dynamic_bean-482422aabcccdac7d7fbd6d369cdbe4c.jpg)

column-qualified format for map

![title_map](/en/assets/images/title_map-13d12e479c22398dc7b73af7e44c3232.jpg)

multiline field

![map](/en/assets/images/multiline-d4bd4a85c32fa4b9978c22cd9d0adaa9.jpg)

Data label filtering

![tag](/en/assets/images/tag-e58c3cc27b698633de18a8f060eb96a3.jpg)

## Overview of other formats​

Take behavior tree as an example to show how to configure behavior tree configuration in json format. For xml, lua, yaml and other formats, please refer to [Detailed Documentation](http://localhost:3000/docs/intro).
    
    
    {  
       "id": 10002,  
       "name": "random move",  
       "desc": "demo behavior tree",  
       "executor": "SERVER",  
       "blackboard_id": "demo",  
       "root": {  
         "$type": "Sequence",  
         "id": 1,  
         "node_name": "test",  
         "desc": "root",  
         "services": [],  
         "decorators": [  
           {  
             "$type": "UeLoop",  
             "id": 3,  
             "node_name": "",  
             "flow_abort_mode": "SELF",  
             "num_loops": 0,  
             "infinite_loop": true,  
             "infinite_loop_timeout_time": -1  
           }  
         ],  
         "children": [  
           {  
             "$type": "UeWait",  
             "id": 30,  
             "node_name": "",  
             "ignore_restart_self": false,  
             "wait_time": 1,  
             "random_deviation": 0.5,  
             "services": [],  
             "decorators": []  
           },  
           {  
             "$type": "MoveToRandomLocation",  
             "id": 75,  
             "node_name": "",  
             "ignore_restart_self": false,  
             "origin_position_key": "x5",  
             "radius": 30,  
             "services": [],  
             "decorators": []  
           }  
         ]  
       }  
    }  
    

## code usage preview​

Here we only briefly show the usage of c#, typescript, go, and c++ languages in development. For more languages and more detailed usage examples and codes, see [Example Project](https://gitee.com/focus-creative-games/luban_examples).

  * C# usage example


    
    
    // One line of code can load all configurations. cfg.Tables contains an instance field for all tables.  
    var tables = new cfg.Tables(file => return new ByteBuf(File.ReadAllBytes($"{gameConfDir}/{file}.bytes")));  
    // access a singleton table  
    Console.WriteLine(tables.TbGlobal.Name);  
    // access normal key-value table  
    Console.WriteLine(tables.TbItem.Get(12).Name);  
    // support operator [] usage  
    Console.WriteLine(tables.TbMail[1001].Desc);  
    

  * example of typescript usage


    
    
    // One line of code can load all configurations. cfg.Tables contains an instance field for all tables.  
    let tables = new cfg. Tables(f => JsHelpers. LoadFromFile(gameConfDir, f))  
    // access a singleton table  
    console.log(tables.TbGlobal.name)  
    // access normal key-value table  
    console.log(tables.TbItem.get(12).Name)  
    

  * go usage example


    
    
    // One line of code can load all configurations. cfg.Tables contains an instance field for all tables.  
    if tables , err := cfg.NewTables(loader) ; err != nil {  
      println(err. Error())  
      return  
    }  
    // access a singleton table  
    println(tables. TbGlobal. Name)  
    // access normal key-value table  
    println(tables. TbItem. Get(12). Name)  
    

  * c++ usage example


    
    
         cfg::Tables tables;  
         if (!tables.load([](ByteBuf& buf, const std::string& s) { return buf.loadFromFile("../GenerateDatas/bytes/" + s + ".bytes"); }))  
         {  
             std::cout << "== load fail == " << std::endl;  
             return;  
         }  
         std::cout << tables. TbGlobal->name << std::endl;  
         std::cout << tables.TbItem.get(12)->name << std::endl;  
    

## license​

Luban is licensed under the [MIT](https://github.com/focus-creative-games/luban/blob/main/LICENSE) license

