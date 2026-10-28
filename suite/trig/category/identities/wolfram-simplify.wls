(* assume-eval: suite trig · category identities · system wolfram-simplify (5 cases listed) *)
(* 5 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case trig-double-01 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184527 answered true (solved) *)
Print["== trig-double-01 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[z, Complexes]);
  Residual = (Sin[2*z]) - (2*(Sin[z]*Cos[z]));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-184527 answered true (solved)"];

(* ---- case trig-double-02 · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184527 answered null (no verdict) *)
Print["== trig-double-02 · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x < 1));
  Residual = (Sin[2*x]) - (2*Sin[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261028-184527 answered null (no verdict)"];

(* ---- case trig-pyth-01 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184527 answered true (solved) *)
Print["== trig-pyth-01 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[z, Complexes]);
  Residual = (Sin[z]*Sin[z] + Cos[z]*Cos[z]) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-184527 answered true (solved)"];

(* ---- case trig-sqrt-01 · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184527 answered null (declined correctly) *)
Print["== trig-sqrt-01 · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sqrt[1 - Sin[x]*Sin[x]]) - (Cos[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-184527 answered null (declined correctly)"];

(* ---- case trig-tan-01 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184527 answered true (solved) *)
Print["== trig-tan-01 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0));
  Residual = (Tan[x]) - (Sin[x]/Cos[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-184527 answered true (solved)"];
