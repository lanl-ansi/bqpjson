% id : 0
% description : this case tests the hfs translator.  both in recovering intger coefficents and computing an effective chimera degree.
% 
% chimera_cell_size : 8
% chimera_degree : 12

set of int: Domain = {0,1};
float: offset = 2.375;
float: scale = 1.0;

var Domain: x0;
var Domain: x1;
var Domain: x2;
var Domain: x3;
var Domain: x4;
var Domain: x5;
var Domain: x6;
var Domain: x7;
var Domain: x8;
var Domain: x9;
var Domain: x10;
var Domain: x11;
var Domain: x12;
var Domain: x13;
var Domain: x14;
var Domain: x15;
var Domain: x96;
var Domain: x97;
var Domain: x98;
var Domain: x99;
var Domain: x100;
var Domain: x101;
var Domain: x102;
var Domain: x103;
var Domain: x104;
var Domain: x105;
var Domain: x106;
var Domain: x107;
var Domain: x108;
var Domain: x109;
var Domain: x110;
var Domain: x111;

var float: objective = 1.0*x0 + -1.0*x1 + 2.5*x2 + -4.75*x3 + -1.0*x4 + 2.0*x5 + 1.75*x6 + -2.25*x7 + 2.5*x8 + -3.5*x9 + 3.0*x10 + -1.5*x11 + -2.75*x12 + 1.25*x13 + 4.75*x14 + 1.25*x15 + -2.0*x96 + 3.5*x97 + 1.25*x98 + 3.0*x99 + 5.5*x100 + 1.0*x101 + 1.75*x102 + -0.75*x103 + -3.25*x104 + 1.25*x105 + -4.75*x106 + -5.0*x107 + -3.0*x108 + -5.0*x109 + -1.5*x110 + -3.5*x111 + 3.0*x0*x4 + -3.0*x0*x5 + 1.5*x0*x6 + 2.0*x0*x7 + -3.0*x0*x96 + 3.5*x1*x4 + 0.5*x1*x5 + -2.0*x1*x6 + -0.5*x1*x7 + -2.0*x1*x97 + -3.0*x2*x4 + -2.5*x2*x5 + -1.0*x2*x6 + -0.5*x2*x7 + 1.0*x2*x98 + -3.5*x3*x4 + 3.0*x3*x5 + 3.5*x3*x6 + 2.0*x3*x7 + 3.0*x3*x99 + 3.0*x4*x12 + -1.5*x5*x13 + -2.0*x6*x14 + 2.0*x7*x15 + 2.0*x8*x12 + -1.5*x8*x13 + -1.5*x8*x14 + -3.5*x8*x15 + -3.5*x8*x104 + -1.0*x9*x12 + 3.0*x9*x13 + 3.0*x9*x14 + 1.0*x9*x15 + -1.5*x9*x105 + -3.5*x10*x12 + -1.0*x10*x13 + -3.5*x10*x14 + 3.0*x10*x15 + 2.0*x10*x106 + 2.0*x11*x12 + 0.5*x11*x13 + -3.0*x11*x14 + -3.0*x11*x15 + 3.5*x11*x107 + 1.5*x96*x100 + 3.0*x96*x101 + -1.0*x96*x102 + 0.5*x96*x103 + -2.5*x97*x100 + -3.5*x97*x101 + -4.0*x97*x102 + 1.0*x97*x103 + -1.5*x98*x100 + -4.0*x98*x101 + 2.0*x98*x102 + 1.5*x98*x103 + -2.0*x99*x100 + -2.5*x99*x101 + -1.5*x99*x102 + -1.5*x99*x103 + -4.0*x100*x108 + 4.0*x101*x109 + -1.0*x102*x110 + 1.5*x103*x111 + 3.0*x104*x108 + 3.5*x104*x109 + 2.0*x104*x110 + 3.5*x104*x111 + 3.0*x105*x108 + 3.0*x105*x109 + -4.0*x105*x110 + -4.0*x105*x111 + 4.0*x106*x108 + 1.5*x106*x109 + 4.0*x106*x110 + 2.0*x106*x111 + -2.5*x107*x108 + 1.0*x107*x109 + 3.0*x107*x110 + 1.0*x107*x111;

solve minimize objective;

output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111])];
