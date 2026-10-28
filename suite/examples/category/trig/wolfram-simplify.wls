(* assume-eval: suite examples · category trig · system wolfram-simplify (2 cases listed) *)
(* 2 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case demo-eq-trig-01 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184451 answered true (solved) *)
Print["== demo-eq-trig-01 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Sin[x]^2 + Cos[x]^2) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-184451 answered true (solved)"];

(* ---- case demo-eq-trig-02 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-184451 answered true (solved) *)
Print["== demo-eq-trig-02 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (2*Sin[x]*Cos[x]) - (Sin[2*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-184451 answered true (solved)"];
