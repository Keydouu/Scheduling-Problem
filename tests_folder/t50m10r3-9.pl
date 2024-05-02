%% ****  Testsuite  ****
% Number of tests                  : 50
% Number of machines               : 10
% Number of resources              : 3
% Number of families               : 1
% Prob that a test use a resource  : 30%
% Minimum test duration            : 1
% Maximim test duration            : 800
% MPri                             : 40%

test( 't1', 357, [], [], 'fam1', 1 ).
test( 't2', 411, [], [], 'fam1', 1 ).
test( 't3', 472, [], ['r2'], 'fam1', 1 ).
test( 't4', 311, [], [], 'fam1', 1 ).
test( 't5', 552, [], ['r2','r1'], 'fam1', 1 ).
test( 't6', 533, [], [], 'fam1', 1 ).
test( 't7', 197, [], ['r2'], 'fam1', 1 ).
test( 't8', 347, ['m10','m4'], [], 'fam1', 1 ).
test( 't9', 575, [], ['r2','r3'], 'fam1', 1 ).
test( 't10', 238, [], [], 'fam1', 1 ).
test( 't11', 463, ['m1'], ['r2'], 'fam1', 1 ).
test( 't12', 116, [], [], 'fam1', 1 ).
test( 't13', 194, [], [], 'fam1', 1 ).
test( 't14', 15, ['m3'], ['r2','r1','r3'], 'fam1', 1 ).
test( 't15', 688, [], ['r1','r2','r3'], 'fam1', 1 ).
test( 't16', 101, ['m7'], [], 'fam1', 1 ).
test( 't17', 151, [], ['r1','r2'], 'fam1', 1 ).
test( 't18', 71, ['m6','m9','m4'], [], 'fam1', 1 ).
test( 't19', 465, [], [], 'fam1', 1 ).
test( 't20', 132, [], [], 'fam1', 1 ).
test( 't21', 585, [], ['r3','r2','r1'], 'fam1', 1 ).
test( 't22', 337, ['m8','m6'], [], 'fam1', 1 ).
test( 't23', 10, [], [], 'fam1', 1 ).
test( 't24', 301, [], [], 'fam1', 1 ).
test( 't25', 518, [], [], 'fam1', 1 ).
test( 't26', 14, [], ['r1','r2'], 'fam1', 1 ).
test( 't27', 139, [], [], 'fam1', 1 ).
test( 't28', 365, ['m1'], ['r3','r2'], 'fam1', 1 ).
test( 't29', 439, [], [], 'fam1', 1 ).
test( 't30', 42, [], [], 'fam1', 1 ).
test( 't31', 442, [], ['r2','r1','r3'], 'fam1', 1 ).
test( 't32', 628, ['m6','m5','m8','m10'], [], 'fam1', 1 ).
test( 't33', 672, ['m5'], ['r2','r3'], 'fam1', 1 ).
test( 't34', 252, ['m7'], [], 'fam1', 1 ).
test( 't35', 729, [], [], 'fam1', 1 ).
test( 't36', 792, ['m8','m5','m3'], [], 'fam1', 1 ).
test( 't37', 262, [], [], 'fam1', 1 ).
test( 't38', 1, [], ['r2','r3'], 'fam1', 1 ).
test( 't39', 796, [], ['r1','r3'], 'fam1', 1 ).
test( 't40', 796, [], [], 'fam1', 1 ).
test( 't41', 687, [], [], 'fam1', 1 ).
test( 't42', 424, [], ['r3','r1'], 'fam1', 1 ).
test( 't43', 492, [], [], 'fam1', 1 ).
test( 't44', 525, [], ['r2','r1'], 'fam1', 1 ).
test( 't45', 116, [], [], 'fam1', 1 ).
test( 't46', 784, [], ['r3','r2','r1'], 'fam1', 1 ).
test( 't47', 304, [], [], 'fam1', 1 ).
test( 't48', 645, ['m3','m7'], [], 'fam1', 1 ).
test( 't49', 690, [], ['r1','r2','r3'], 'fam1', 1 ).
test( 't50', 640, ['m8'], [], 'fam1', 1 ).

embedded_board( 'm1').
embedded_board( 'm2').
embedded_board( 'm3').
embedded_board( 'm4').
embedded_board( 'm5').
embedded_board( 'm6').
embedded_board( 'm7').
embedded_board( 'm8').
embedded_board( 'm9').
embedded_board( 'm10').

testsetup( 'fam1', 0 ).

resource( 'r1', 1).
resource( 'r2', 1).
resource( 'r3', 1).
