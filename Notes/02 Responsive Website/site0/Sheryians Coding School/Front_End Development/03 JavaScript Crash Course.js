// javascript has interpriter and not compailer
// word vs keyword
// eg, boy == word | anything doesent have a meaning in js is word
// for == keyword | and anything does have a meaning in js is keyword

// var const let
// variables and constants
// used to stored data 
var a = "Hello";
const b = "World";
let c = 12;
console.log(a, b, c)

// hoisting :- variable and function are hoisted which means there declaration is moved on the top of the code. 
console.log(hoi);  
// undefine | undefine != notdefine 
var hoi = 34;
console.log(hoi);
// 34

// types in js
// 1. primitive and 2. reference
// primitive = numbers, string, null, undifined, boolean
// reference = [], (), {}
// => aisi koi bhi value jisko copy karane par real value copy nahi hota, balki us main value ka reference pass hojata hai, use ham reference value kahate hai. Aur jise copy karane par real copy ho jaye wo value primitive type value hoti hai.
var a1 = 12;
var b1 = a1;
// console.log(a1, b1);

b1 = b1 + 1;
// console.log(a1, b1);

var c1 = [12, 13, 14, 15];
var d1 = c1;
// console.log(c1, d1);

d1.pop();
// console.log(c1, d1);

// conditionals - if else else-if 
// if(condition){ // true or false

// } 
// else{

// }

// else-if
// if(condition1){ // true or false

// } 
// else if(condition2){

// }
// else if(condition3){

// }
// else if(condition4){

// }
// else{

// }

// loop - for
// for(Start; end; change){   
// }
for(var i = 0; i<11; i++){
    console.log(i);
}

for(var i = 25; i<51; i++){
    console.log(i);
}

// loop - while
var a = 12;
while(a<20){
    console.log(a);
    a++;
}