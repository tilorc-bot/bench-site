(* assume-eval: suite simplipy · case sp-acj4-424-condf · all Wolfram systems *)
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

(* ---- case sp-acj4-424-condf · expected false · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-214714 answered null (no verdict) *)
Print["== sp-acj4-424-condf · wolfram-fullsimplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Tanh[ArcSinh[Abs[x]]]) - (Cos[ArcTan[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-fullsimplify-20261019-214714 answered null (no verdict)"];

(* ---- case sp-acj4-424-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-214702 answered null (no verdict) *)
Print["== sp-acj4-424-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Tanh[ArcSinh[Abs[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261019-214702 answered null (no verdict)"];

(* ---- case sp-acj4-424-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-214647 answered null (no verdict) *)
Print["== sp-acj4-424-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Tanh[ArcSinh[Abs[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261019-214647 answered null (no verdict)"];
