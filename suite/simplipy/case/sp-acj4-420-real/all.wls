(* assume-eval: suite simplipy · case sp-acj4-420-real · all Wolfram systems *)
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

(* ---- case sp-acj4-420-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-420-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-420-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-420-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-420-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
Print["== sp-acj4-420-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];
