Implementation
==============

.. toctree::
   :maxdepth: 2

General
-------

Object
++++++

1. 每个Object用两个字表示，第一个字用于记录类型，第二个字用于存储数据。类型与存储数据关系如下：

    =========  =========== ======
       类型         数据     类型值
    =========  =========== ======
    整数         直接存储      0
    字符串       指针         2
    对象         指针         3
    函数         指针         4
    null        无           5
    undefined   无           6
    readInt     无           7
    readStr     无           8
    show        无           9
    =========  =========== ======


2. 每个Object可用一个指针访问。

3. 对于字符串，其数据指针指向一个0结尾的字符串，字节顺序为从低地址至高地址，四字节对齐。

4. 对于对象，其指针指向一个链表，每个节点有三个域。

    - 第一个存储着key，内容为指向一个字符串或是数的指针。

    - 第二个存储着value，内容为指向一个对象的指针。

    - 第三个为指向下一个节点的指针，若没有下一个节点则为0。

5. 每个对象有一个隐含的属性constructor，将会指向其将其new出来的构造函数。当属性查找不到时会沿着prototype向上找。初始时会有Object构造函数作为所有对象的原型。整数、浮点数、布尔、字符串、null、undefined没有constructor域。

Function
++++++++

1. 每个函数对象有五个特有的属性。

    - 其一为address，内容为一个整数，内容为该函数的入口地址。
    - 其二为scope，内容为一个对象，用于保存函数闭包里的变量。
    - 其三为outer，内容为一个函数，用于记录定义这个函数的外部环境。
    - 其四为prototype，用于记录对象的原型。
    - 其五为arguments，用于记录所有参数对应的offset。

2. 在函数中访问一个变量时，会首先在本函数的arguments中查找，若找不到则会scope中查找，若找不到则会到沿着outer向上查找。

Runtime
+++++++

1. 每当调用函数时，调用者会将fp推进堆栈，然后将fp指向当前sp的位置。之后将返回地址、调用函数、this指针推入堆栈，预留返回值空间，之后逐个推入参数。

::

        |                |
         ----------------
        |     old fp     |
         ----------------  
        |   return addr  |  <--- fp
         ----------------  
        |    function    |       
         ----------------           
        |      this      |          
         ----------------        
        |  return value  |
         ---------------- 
        |      arg1      |
         ----------------                                                     
        |      arg2      |
         ---------------- 
        |                |  <--- sp
                                                                

Virtual Machine
---------------

Instruction Set
+++++++++++++++

==========  ===========================  ================================================================================
指令名       指令格式                      含义
==========  ===========================  ================================================================================
newfunc     newfunc <rd>, <label>        创建一个新的函数，label为函数的入口
newobj      newobj <rd>                  创建一个新的对象
getfield    getfield <rd>, <rs>, <rt>    获取一个对象中属性的指针，rs为对象，rt为属性名字符串的指针，若属性不存在则会被新建
findfield   findfield <rd>, <rs>, <rt>   获取一个对象中属性的指针，若属性不存在则会报错
getvar      getvar <rd>, <rs>            获取当前函数中变量的指针，rs为变量名字符串的指针，若变量不存在则会被新建
findvar     findvar <rd>, <rs>           获取当前函数中变量的指针，若变量不存在则会报错
typeof      typeof <rd>, <rs>            获取一个对象中类型，rd为指向类型字符串对象的指针
cmp         cmp <rd>, <rs>, <rt>         比较两个对象是否相同，若是则rd为指向整数1的指针，否则rd为指向整数0的指针     
slt         slt <rd>, <rs>, <rt>         若rs所指向的对象小于rt所指向的对象，则rd为指向整数1的指针，否则rd为指向整数0的指针
add         add <rd>, <rs>, <rt>     
sub         sub <rd>, <rs>, <rt>
mul         mul <rd>, <rs>, <rt>
div         div <rd>, <rs>, <rt>
mod         mod <rd>, <rs>, <rt>
and         and <rd>, <rs>, <rt>
or          or  <rd>, <rs>, <rt>
xor         xor <rd>, <rs>, <rt>
not         not <rd>, <rs>
sra         sra <rd>, <rs>, <rt>
srl         srl <rd>, <rs>, <rt>
sll         sll <rd>, <rs>, <rt>
bez         bez <rs>, <label>            若rs所指向的对象为假则跳转到label
bnz         bnz <rs>, <label>            若rs所指向的对象为真则跳转到label
ld          ls <rd>, <offset>(<rs>)      将[rs+offset]的值存入rd中
st          st <rd>, <offset>(<rs>)      将rd中的值存入[rs+offset]
la          la <rd> <label>              将label的地址存入rd
j           j <label>
jalr        jalr <rd>                    跳转到rd指向的函数，同时把返回地址存到fp所指的内存位置
move        move <rd>, <rs>
ret         ret                          从函数中返回
==========  ===========================  ================================================================================

Predefined Environment
++++++++++++++++++++++

1. init函数，包含整个程序的作用域。

Memory Layout
+++++++++++++

1. 0x00000000 - 0x0FFFFFFF：代码区
2. 0x10000000 - 0x1FFFFFFF：编译生成的数据区
3. 0x20000000 - 0x2FFFFFFF：堆栈区，由高地址向地地址
4. 0x30000000 -           ：堆，用于内存动态分配

Memory Content
++++++++++++++

1. 每个地址对应的content都有一个type键，用于表示该地址对应数据的类型

    ========= ======
       类型     类型值
    ========= ======
    内存值      0
    对象        1
    指令        2
    属性        3
    ========= ======

所有内存值里都具有content键，用于存储该地址所对应的值。若类型为对象，则其中还有object键。若类型为指令，则其中还有inst键。若类型为属性，则其中还有property键。
