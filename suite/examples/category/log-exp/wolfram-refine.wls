(* assume-eval: suite examples · category log-exp · system wolfram-refine (2 cases listed) *)
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

(* ---- case demo-eq-log-01 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-184500 answered true (solved) *)
Print["== demo-eq-log-01 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0));
  Residual = (Log[Exp[x]]) - (x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-184500 answered true (solved)"];

(* ---- case demo-eq-pow-01 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-184500 answered true (solved) *)
Print["== demo-eq-pow-01 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[n, Integers]);
  Residual = ((-1)^(2*n)) - (1);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-184500 answered true (solved)"];
