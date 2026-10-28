(* assume-eval: suite examples · category parity · all Wolfram systems (5 cases listed) *)
(* 15 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

Begin["AEScript`"];
verdict[out_, expected_String, stored_String] := Module[{answer, got, outcome},
  answer = If[ListQ[out] && Length[out] > 0, Last[out], Null];
  got = Which[answer === True, "true", answer === False, "false", True, "null"];
  outcome = Which[got === "null", If[expected === "contingent", "declined correctly", "no verdict"],
    got === expected, "solved", True, "wrong"];
  Print[out];
  Print["verdict: " <> got <> " (expected " <> expected <> ": " <> outcome <> "; " <> stored <> ")"];
  got];
End[];

(* ---- case demo-parity-01 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261028-184509 answered true (solved) *)
Print["== demo-parity-01 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[((n) - 1)/2, Integers]);
  Residual = ((-1)^(n + 1)) - (1);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261028-184509 answered true (solved)"];

(* ---- case demo-parity-01 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-184500 answered true (solved) *)
Print["== demo-parity-01 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[((n) - 1)/2, Integers]);
  Residual = ((-1)^(n + 1)) - (1);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-184500 answered true (solved)"];

(* ---- case demo-parity-01 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184451 answered true (solved) *)
Print["== demo-parity-01 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[((n) - 1)/2, Integers]);
  Residual = ((-1)^(n + 1)) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-184451 answered true (solved)"];

(* ---- case demo-parity-02 · expected false · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261028-184509 answered false (solved) *)
Print["== demo-parity-02 · wolfram-fullsimplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[m, Integers]) && (Element[((n) - 1)/2, Integers]) && (Element[((m) - 1)/2, Integers]);
  Residual = ((-1)^(n*m)) - (1);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-fullsimplify-20261028-184509 answered false (solved)"];

(* ---- case demo-parity-02 · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-184500 answered false (solved) *)
Print["== demo-parity-02 · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[m, Integers]) && (Element[((n) - 1)/2, Integers]) && (Element[((m) - 1)/2, Integers]);
  Residual = ((-1)^(n*m)) - (1);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-184500 answered false (solved)"];

(* ---- case demo-parity-02 · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184451 answered false (solved) *)
Print["== demo-parity-02 · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[m, Integers]) && (Element[((n) - 1)/2, Integers]) && (Element[((m) - 1)/2, Integers]);
  Residual = ((-1)^(n*m)) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261028-184451 answered false (solved)"];

(* ---- case demo-parity-03 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261028-184509 answered true (solved) *)
Print["== demo-parity-03 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]);
  Residual = ((-1)^(n*(n + 1))) - (1);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261028-184509 answered true (solved)"];

(* ---- case demo-parity-03 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-184500 answered true (solved) *)
Print["== demo-parity-03 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]);
  Residual = ((-1)^(n*(n + 1))) - (1);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-184500 answered true (solved)"];

(* ---- case demo-parity-03 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184451 answered true (solved) *)
Print["== demo-parity-03 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]);
  Residual = ((-1)^(n*(n + 1))) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-184451 answered true (solved)"];

(* ---- case demo-parity-04 · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261028-184509 answered null (declined correctly) *)
Print["== demo-parity-04 · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[(n)/2, Integers]);
  Residual = (I^n) - (1);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261028-184509 answered null (declined correctly)"];

(* ---- case demo-parity-04 · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-184500 answered null (declined correctly) *)
Print["== demo-parity-04 · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[(n)/2, Integers]);
  Residual = (I^n) - (1);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-184500 answered null (declined correctly)"];

(* ---- case demo-parity-04 · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184451 answered null (declined correctly) *)
Print["== demo-parity-04 · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[(n)/2, Integers]);
  Residual = (I^n) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-184451 answered null (declined correctly)"];

(* ---- case demo-parity-05 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261028-184509 answered true (solved) *)
Print["== demo-parity-05 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[m, Integers]) && (Element[((n) - 1)/2, Integers]) && (Element[((m) - 1)/2, Integers]);
  Residual = ((-1)^(n*m)) - (-1);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261028-184509 answered true (solved)"];

(* ---- case demo-parity-05 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-184500 answered true (solved) *)
Print["== demo-parity-05 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[m, Integers]) && (Element[((n) - 1)/2, Integers]) && (Element[((m) - 1)/2, Integers]);
  Residual = ((-1)^(n*m)) - (-1);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-184500 answered true (solved)"];

(* ---- case demo-parity-05 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184451 answered true (solved) *)
Print["== demo-parity-05 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]) && (Element[m, Integers]) && (Element[((n) - 1)/2, Integers]) && (Element[((m) - 1)/2, Integers]);
  Residual = ((-1)^(n*m)) - (-1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-184451 answered true (solved)"];
