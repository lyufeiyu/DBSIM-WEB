在学习 Vue.js 之前，学习 ES6（ECMAScript 2015）是很有必要的，原因如下：

📒官方推荐：Vue.js 官方文档和社区中广泛使用了 ES6 的语法和特性。通过学习 ES6，您将能更好地理解和应用 Vue.js 中的示例代码和文档。

📒新特性支持：ES6 引入了许多强大的新特性，如箭头函数、解构赋值、模块化、Promise、Class、模板字符串等。这些特性可以提高开发效率，使代码更简洁、可读性更好，并且可以充分利用 JavaScript 的功能。

📒提升开发效率：ES6 提供了许多语言层面的功能和优化，使得开发人员可以更快、更高效地编写和组织代码。比如箭头函数可以简化函数的定义和使用，解构赋值可以方便地从对象或数组中提取值。

📒模块化支持：ES6 引入了模块化的概念，使得代码可以按模块组织、导入和导出。这种模块化的开发方式可以提高代码的可维护性和可测试性，也符合现代化的开发规范。

📒兼容性和未来发展：ES6 是 JavaScript 的下一代标准，浏览器厂商和开发者社区都在积极支持和推广。掌握 ES6 让您能够编写更先进的 JavaScript 代码，并且能够顺利迁移到未来的 JavaScript 版本，同时还能兼顾旧版本的浏览器兼容性。

总的来说，学习 ES6 可以让您更好地理解和应用 Vue.js，同时也提升了您作为前端开发者的技能水平和竞争力。它是现代 JavaScript 开发的重要基础，对于学习和掌握任何现代的前端框架和工具都是非常有帮助的。

~~~
注意注意，下面这只是基础内容，其他的用到再去查阅资料。
~~~

# ES6基础内容
### 简介
ES6全称ECMAScript 6，是浏览器脚本语言的一种标准，是Javascript的规格。JavaScript是ECMAScript的一种实现。
### let的使用以及和var的区别
var 定义在函数外面就是全局变量，定义在函数内就是局部变量。
let 只在代码块中有效
```JS
<script>
   //1 创建代码块，定义变量
   {
       var a = 10
       let b = 20
   }
   //2在代码块 外面输出
   console.log(a)   //10
   console.log(b)  // not defined

	function hello(){
		var c=20;
		console.log("in"+c);  // in20
		console.log("in"+a);  // in10
		let d=2;
	} 
	console.log(d); // not defined
	hello();   
	console.log("out"+c);  // not defined

//var 定义在函数外面就是全局变量，定义在函数内就是局部变量。
//let 只在代码块中有效
</script>
```
### let 只能被声明一次
```JS
<script>
   var a = 1
   var a = 2

   let m = 10
   let m = 20 //Uncaught SyntaxError: Identifier 'm' has already been declared

    console.log(a)
    console.log(m) 
    
    //let 只能被声明一次
</script>
```

### const声明常量
```JS
<script>
    //定义常量
    const PI = "3.1415"
    //常量值一旦定义，不能改变
    PI = 3  //Uncaught TypeError: Assignment to constant variable.

    //定义常量必须初始化
    const AA  //Uncaught SyntaxError: Missing initializer in const declaration
</script>
```
### 数组
```JS
<script>
    //传统写法
    let a=1,b=2,c=3
    console.log(a, b, c)

    //es6写法
    let [x,y,z] = [10,20,30]
    console.log(x, y, z)
    
</script>
```

### 对象
- 获取对象属性
```JS
<script>
    //定义对象
    let student = {"name":"tom","age":20}

    //传统从对象里面获取值
    let name1 = student.name
    let age1 = student.age
    console.log(name1+"=="+age1)

    //es6获取对象值
    let {name,age} = user
    console.log(name+"**"+age)

//需要了解这个用法,看到后知道什么意思，我感觉这种用的少吧
</script>
```
### 定义对象
```JS
<script>
    const age = 12
    const name = "lucy"

    //传统方式定义对象
    const student = {name:name,age:age}
    console.log(student)

    //es6定义变量
    const student= {name,age}
    console.log(student)

</script>
```

### 对象复制与合并
```JS
<script>
     //1 对象复制
     let person1 = {"name":"lucy","age":20}
     let person2 = {...person1}   

     console.log(person2)   
     //2 对象合并
     let name = {name:'mary'}
     let age = {age:30}
     let student = {...name,...age}
     console.log(student)
</script>
```

### 模板字符串
注意这里" ` "不是单引号，是~那个键上面的符号`
```JS
<script>
    //1 使用`符号实现换行  
    let str1 = `hello,
        es6 demo up!`
    console.log(str1)   结果也换行了

    //2 在`符号里面使用表达式获取变量值
    let name = "Mike"
    let age = 20

    let str2 = `hello,${name},age is ${age+1}`
    //console.log(str2)

    //3 在`符号调用方法
    function f() {
        return "hello f1"
    }

    let str3 = `demo, ${f()}`
    console.log(str3)
</script>
```

### 定义方法
```JS
<script>
    //传统方式定义的方法
    const person1 = {
        sayhello:function(){
            console.log("hello")
        }
    }

    //调用
    person1.sayHello()

    //es6
    const person2 = {
        sayHi(){
            console.log("hello")
        }
    }
    person2.sayHello()

</script>
```

### 箭头函数
方法名=参数=>方法
```JS
<script>
    //1 传统方式创建方法
    var f1 = function(m) {
        return m
    }
    console.log(f1(2))

    //使用箭头函数改造 方法名=参数=方法
    var f2 = m => m
   // console.log(f2(8))

   //2 复杂一点方法
   var f3 = function(a,b) {
   		var	c=a+b;
       return c+2;
   }
   console.log(f3(1,2))

   //箭头函数简化
   var f4 = (a,b) => (c=a+b,c+2)
   console.log(f4(2,2))//6
</script>
```


