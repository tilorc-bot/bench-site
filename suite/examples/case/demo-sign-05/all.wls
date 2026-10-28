(* assume-eval: suite examples · case demo-sign-05 · all Wolfram systems *)
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

(* ---- case demo-sign-05 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261028-000822 answered true (solved) *)
Print["== demo-sign-05 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[y, Reals]) && ((Element[x, Reals] && x > 0)) && ((Element[y, Reals] && y < 0));
  Residual = (Abs[x - y]) - (x - y);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261028-000822 answered true (solved)"];

(* ---- case demo-sign-05 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-000813 answered true (solved) *)
Print["== demo-sign-05 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[y, Reals]) && ((Element[x, Reals] && x > 0)) && ((Element[y, Reals] && y < 0));
  Residual = (Abs[x - y]) - (x - y);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-000813 answered true (solved)"];

(* ---- case demo-sign-05 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-000740 answered true (solved) *)
Print["== demo-sign-05 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[y, Reals]) && ((Element[x, Reals] && x > 0)) && ((Element[y, Reals] && y < 0));
  Residual = (Abs[x - y]) - (x - y);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-000740 answered true (solved)"];
