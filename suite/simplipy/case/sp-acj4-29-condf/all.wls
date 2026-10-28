(* assume-eval: suite simplipy · case sp-acj4-29-condf · all Wolfram systems *)
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

(* ---- case sp-acj4-29-condf · expected false · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261028-160039 answered null (no verdict) *)
Print["== sp-acj4-29-condf · wolfram-fullsimplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && ((Power[x, 3] != 0));
  Residual = (3*Log[x]) - (Log[x^3]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-fullsimplify-20261028-160039 answered null (no verdict)"];

(* ---- case sp-acj4-29-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-160022 answered null (no verdict) *)
Print["== sp-acj4-29-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && ((Power[x, 3] != 0));
  Residual = (3*Log[x]) - (Log[x^3]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-160022 answered null (no verdict)"];

(* ---- case sp-acj4-29-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-160001 answered null (no verdict) *)
Print["== sp-acj4-29-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && ((Power[x, 3] != 0));
  Residual = (3*Log[x]) - (Log[x^3]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261028-160001 answered null (no verdict)"];
