%% ****  Testsuite  ****
% Number of tests                  : 40
% Number of machines               : 10
% Number of resources              : 3
% Number of families               : 1
% Prob that a test use a resource  : 30%
% Minimum test duration            : 1
% Maximim test duration            : 800
% MPri                             : 40%

test( 't1', 568, [], [], 'fam1', 1 ).
test( 't2', 669, [], ['r3'], 'fam1', 1 ).
test( 't3', 688, [], [], 'fam1', 1 ).
test( 't4', 709, ['m7'], [], 'fam1', 1 ).
test( 't5', 505, ['m3'], [], 'fam1', 1 ).
test( 't6', 683, [], [], 'fam1', 1 ).
test( 't7', 20, [], [], 'fam1', 1 ).
test( 't8', 250, ['m6'], [], 'fam1', 1 ).
test( 't9', 235, [], [], 'fam1', 1 ).
test( 't10', 651, [], [], 'fam1', 1 ).
test( 't11', 477, ['m10'], [], 'fam1', 1 ).
test( 't12', 227, [], [], 'fam1', 1 ).
test( 't13', 464, [], [], 'fam1', 1 ).
test( 't14', 257, [], [], 'fam1', 1 ).
test( 't15', 80, ['m2'], [], 'fam1', 1 ).
test( 't16', 592, [], [], 'fam1', 1 ).
test( 't17', 376, ['m9'], [], 'fam1', 1 ).
test( 't18', 541, [], [], 'fam1', 1 ).
test( 't19', 215, [], [], 'fam1', 1 ).
test( 't20', 645, [], [], 'fam1', 1 ).
test( 't21', 624, [], ['r2'], 'fam1', 1 ).
test( 't22', 463, ['m1'], [], 'fam1', 1 ).
test( 't23', 549, [], [], 'fam1', 1 ).
test( 't24', 647, [], ['r1'], 'fam1', 1 ).
test( 't25', 361, [], [], 'fam1', 1 ).
test( 't26', 57, [], ['r3'], 'fam1', 1 ).
test( 't27', 422, [], [], 'fam1', 1 ).
test( 't28', 530, ['m1'], [], 'fam1', 1 ).
test( 't29', 492, [], ['r2'], 'fam1', 1 ).
test( 't30', 306, ['m9','m4','m8'], ['r3'], 'fam1', 1 ).
test( 't31', 519, [], [], 'fam1', 1 ).
test( 't32', 176, [], [], 'fam1', 1 ).
test( 't33', 354, [], ['r1','r2','r3'], 'fam1', 1 ).
test( 't34', 682, [], [], 'fam1', 1 ).
test( 't35', 428, [], [], 'fam1', 1 ).
test( 't36', 340, [], [], 'fam1', 1 ).
test( 't37', 119, ['m1','m6','m4'], ['r3','r2'], 'fam1', 1 ).
test( 't38', 791, [], [], 'fam1', 1 ).
test( 't39', 167, ['m4','m1','m9'], [], 'fam1', 1 ).
test( 't40', 363, [], [], 'fam1', 1 ).

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
