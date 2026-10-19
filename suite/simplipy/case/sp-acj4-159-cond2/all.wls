(* assume-eval: suite simplipy · case sp-acj4-159-cond2 · all Wolfram systems *)
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

(* ---- case sp-acj4-159-cond2 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-214714 answered null (no verdict) *)
Print["== sp-acj4-159-cond2 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x <= 1)) && ((Cosh[x] != 0));
  Residual = (ArcCos[Tanh[Abs[x]]]) - (ArcSin[1/Cosh[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261019-214714 answered null (no verdict)"];

(* ---- case sp-acj4-159-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-214702 answered null (no verdict) *)
Print["== sp-acj4-159-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x <= 1)) && ((Cosh[x] != 0));
  Residual = (ArcCos[Tanh[Abs[x]]]) - (ArcSin[1/Cosh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261019-214702 answered null (no verdict)"];

(* ---- case sp-acj4-159-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-214647 answered null (no verdict) *)
Print["== sp-acj4-159-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x <= 1)) && ((Cosh[x] != 0));
  Residual = (ArcCos[Tanh[Abs[x]]]) - (ArcSin[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261019-214647 answered null (no verdict)"];
