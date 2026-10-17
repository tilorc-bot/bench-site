(* assume-eval: suite simplipy · case sp-acj4-180-cond · all Wolfram systems *)
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

(* ---- case sp-acj4-180-cond · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261017-045037 answered null (no verdict) *)
Print["== sp-acj4-180-cond · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && ((Sinh[ArcCosh[x]] != I)) && ((Sinh[ArcCosh[x]] != (-I))) && ((Cosh[ArcCosh[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCosh[x]]]) - (ArcSin[Tanh[ArcCosh[x]]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261017-045037 answered null (no verdict)"];

(* ---- case sp-acj4-180-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261017-045026 answered null (no verdict) *)
Print["== sp-acj4-180-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && ((Sinh[ArcCosh[x]] != I)) && ((Sinh[ArcCosh[x]] != (-I))) && ((Cosh[ArcCosh[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCosh[x]]]) - (ArcSin[Tanh[ArcCosh[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261017-045026 answered null (no verdict)"];

(* ---- case sp-acj4-180-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261017-045011 answered null (no verdict) *)
Print["== sp-acj4-180-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && ((Sinh[ArcCosh[x]] != I)) && ((Sinh[ArcCosh[x]] != (-I))) && ((Cosh[ArcCosh[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCosh[x]]]) - (ArcSin[Tanh[ArcCosh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261017-045011 answered null (no verdict)"];
