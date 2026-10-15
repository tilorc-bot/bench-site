(* assume-eval: suite simplipy · case sp-acj4-373-cond · all Wolfram systems *)
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

(* ---- case sp-acj4-373-cond · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261015-025100 answered null (declined correctly) *)
Print["== sp-acj4-373-cond · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[Cosh[x], Reals]);
  Residual = (Surd[Cosh[x], 5]) - (Cosh[x]^(1/5));
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261015-025100 answered null (declined correctly)"];

(* ---- case sp-acj4-373-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261015-025050 answered null (declined correctly) *)
Print["== sp-acj4-373-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[Cosh[x], Reals]);
  Residual = (Surd[Cosh[x], 5]) - (Cosh[x]^(1/5));
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261015-025050 answered null (declined correctly)"];

(* ---- case sp-acj4-373-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261015-025035 answered null (declined correctly) *)
Print["== sp-acj4-373-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[Cosh[x], Reals]);
  Residual = (Surd[Cosh[x], 5]) - (Cosh[x]^(1/5));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261015-025035 answered null (declined correctly)"];
