% id : 0
% description : simple model with linear_terms
% 

set of int: Domain = {0,1};
float: offset = 0.0;
float: scale = 1.0;

var Domain: x2;
var Domain: x4;
var Domain: x6;

var float: objective = 1.3*x2 + -0.7*x6;

solve minimize objective;

output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([x2, x4, x6])];
