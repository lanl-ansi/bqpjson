% id : 0
% description : simple model with quadratic_terms and metadata
% 
% some_key_1 : "any value"
% some_key_2 : 0.3
% some_key_3 : null
% some_key_4 : ["one", 2, 3.7, null]
% some_key_5 : {"one": 1, "three": null, "two": 2}

set of int: Domain = {-1,1};
float: offset = 1.23;
float: scale = 2.7;

var Domain: x2;
var Domain: x4;
var Domain: x6;

var float: objective = 1.3*x2 + -0.7*x6 + -0.2*x2*x4 + 1.5*x2*x6;

solve minimize objective;

output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([x2, x4, x6])];
