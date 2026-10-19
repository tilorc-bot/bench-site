(* assume-eval: suite simplipy · case sp-acj4-344-cond2 · all Wolfram systems *)
(* 3 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case sp-acj4-344-cond2 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-214714 answered true (solved) *)
Print["== sp-acj4-344-cond2 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Integers]) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261019-214714 answered true (solved)"];

(* ---- case sp-acj4-344-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-214702 answered true (solved) *)
Print["== sp-acj4-344-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Integers]) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261019-214702 answered true (solved)"];

(* ---- case sp-acj4-344-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-214647 answered true (solved) *)
Print["== sp-acj4-344-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Integers]) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261019-214647 answered true (solved)"];
