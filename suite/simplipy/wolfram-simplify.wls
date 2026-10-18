(* assume-eval: suite simplipy · every case · system wolfram-simplify (307 cases listed) *)
(* 307 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case sp-acj4-0-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-0-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (ArcCosh[Cosh[x]]) - (Abs[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-0-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-0-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCosh[Cosh[x]]) - (Abs[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-1-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-1-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (ArcSin[Abs[x]]) - (Abs[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-1-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-1-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcSin[Abs[x]]) - (Abs[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-1007-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1007-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0/Sin[5]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-102-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-102-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Abs[x]/6) - (Abs[x/-6]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-102-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-102-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Abs[x]/6) - (Abs[x/-6]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-108-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-108-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((Abs[x] != 0));
  Residual = (Abs[x]/x) - (x/Abs[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-108-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-108-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && ((Abs[x] != 0));
  Residual = (Abs[x]/x) - (x/Abs[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-108-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-108-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Abs[x] != 0));
  Residual = (Abs[x]/x) - (x/Abs[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1107-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1107-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (ArcSin[Sin[1/10]]) - (1/10);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1148-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1148-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Cosh[Log[1/4]]) - (17/8);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1149-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1149-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Exp[Abs[Log[2]]]) - (2);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-115-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-115-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((x > 0)) && ((Surd[x, (-4)] != 0));
  Residual = (Log[x]/-4) - (Log[Surd[x, -4]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-116-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-116-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((x > 0)) && ((Surd[x, (-6)] != 0));
  Residual = (Log[x]/-6) - (Log[Surd[x, -6]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1177-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1177-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0^ArcSinh[10]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1195-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1195-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0^ArcTan[7]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-120-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-120-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (Pi/Abs[x]) - (Abs[Pi/x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-120-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-120-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (Pi/Abs[x]) - (Abs[Pi/x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1217-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1217-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0^Exp[-1]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1238-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1238-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0^(1/Pi)) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-124-condf · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-124-condf · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0));
  Residual = (Abs[ArcSin[Tanh[x]]]) - (ArcCos[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-1247-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1247-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0^Log[9]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1254-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1254-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0^Sin[2]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-1258-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-1258-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0^Sin[9]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-127-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-127-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((Exp[x] != 1)) && ((Exp[x] != (-1)));
  Residual = (Abs[ArcTanh[Exp[x]]]) - (ArcTanh[Exp[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-127-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-127-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Exp[x] != 1)) && ((Exp[x] != (-1)));
  Residual = (Abs[ArcTanh[Exp[x]]]) - (ArcTanh[Exp[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-128-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-128-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (Abs[Cos[ArcSin[x]]]) - (Cos[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-128-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-128-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x > 1));
  Residual = (Abs[Cos[ArcSin[x]]]) - (Cos[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-128-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-128-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Abs[Cos[ArcSin[x]]]) - (Cos[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-129-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-129-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != I)) && ((x != (-I)));
  Residual = (Abs[Cos[ArcTan[x]]]) - (Cos[ArcTan[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-130-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-130-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (Abs[Log[Cos[x]]]) - (Log[1/Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-130-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-130-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < (Pi/2))) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (Abs[Log[Cos[x]]]) - (Log[1/Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-130-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-130-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (Abs[Log[Cos[x]]]) - (Log[1/Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-131-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-131-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0));
  Residual = (Abs[Log[Cosh[x]]]) - (Log[Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-131-condf · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-131-condf · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0));
  Residual = (Abs[Log[Cosh[x]]]) - (Log[Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-131-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-131-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cosh[x] != 0));
  Residual = (Abs[Log[Cosh[x]]]) - (Log[Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-132-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-132-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Sin[x] != 0));
  Residual = (Abs[Log[Sin[x]]]) - (-Log[Sin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-132-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-132-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x >= 0)) && ((x <= Pi)) && ((Sin[x] != 0));
  Residual = (Abs[Log[Sin[x]]]) - (-Log[Sin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-132-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-132-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sin[x] != 0));
  Residual = (Abs[Log[Sin[x]]]) - (-Log[Sin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-133-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-133-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0)) && ((Tanh[x] != 0));
  Residual = (Abs[Log[Tanh[x]]]) - (-Log[Tanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-133-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-133-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0)) && ((Tanh[x] != 0));
  Residual = (Abs[Log[Tanh[x]]]) - (-Log[Tanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-133-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-133-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Tanh[x] != 0));
  Residual = (Abs[Log[Tanh[x]]]) - (-Log[Tanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-136-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-136-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x >= 0)) && (((x != 0) || (Re[Exp[1]] > 0)));
  Residual = (Abs[x^Exp[1]]) - (x^Exp[1]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-136-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-136-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[Exp[1]] > 0)));
  Residual = (Abs[x^Exp[1]]) - (x^Exp[1]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-137-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-137-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((x != 0) || (Re[Pi] > 0)));
  Residual = (Abs[x^Pi]) - (x^Pi);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-137-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-137-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x >= 0)) && (((x != 0) || (Re[Pi] > 0)));
  Residual = (Abs[x^Pi]) - (x^Pi);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-137-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-137-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[Pi] > 0)));
  Residual = (Abs[x^Pi]) - (x^Pi);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-14-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-14-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (-Sin[x]) - (Sin[-x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-145-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-145-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (Abs[Sin[ArcCos[x]]]) - (Cos[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-145-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-145-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x > 1));
  Residual = (Abs[Sin[ArcCos[x]]]) - (Cos[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-145-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-145-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Abs[Sin[ArcCos[x]]]) - (Cos[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-147-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-147-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[ArcSinh[x]] != 0)) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Abs[Tanh[ArcSinh[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-147-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-147-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[ArcSinh[x]] != 0)) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Abs[Tanh[ArcSinh[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-151-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-151-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (ArcCos[Cos[ArcSin[x]]]) - (Abs[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-151-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-151-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (ArcCos[Cos[ArcSin[x]]]) - (Abs[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-151-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-151-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Cos[ArcSin[x]]]) - (Abs[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-153-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-153-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (ArcCos[Cos[Cos[x]]]) - (Abs[Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-154-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-154-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (ArcCos[Cos[Sin[x]]]) - (Abs[Sin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-154-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-154-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Cos[Sin[x]]]) - (Abs[Sin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-156-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-156-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (ArcCos[Sin[ArcCos[x]]]) - (Abs[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-156-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-156-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Sin[ArcCos[x]]]) - (Abs[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-159-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-159-cond3 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-159-cond3 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= (Pi/2))) && ((Cosh[x] != 0));
  Residual = (ArcCos[Tanh[Abs[x]]]) - (ArcSin[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-162-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-162-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && (Element[x, Reals]);
  Residual = (ArcCosh[Surd[x, 5]]) - (ArcCosh[x^(1/5)]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-162-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-162-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (ArcCosh[Surd[x, 5]]) - (ArcCosh[x^(1/5)]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-162-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-162-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCosh[Surd[x, 5]]) - (ArcCosh[x^(1/5)]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-165-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-165-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != I)) && ((x != (-I))) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (ArcSin[Cos[ArcTan[x]]]) - (Abs[ArcTan[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-171-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-171-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[Im[x]] < Pi)) && ((Cosh[x] != 0));
  Residual = (ArcSin[Sin[Tanh[x]]]) - (Tanh[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-171-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-171-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0));
  Residual = (ArcSin[Sin[Tanh[x]]]) - (Tanh[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-173-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-173-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0));
  Residual = (ArcSin[Tanh[Abs[x]]]) - (ArcCos[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-176-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-176-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0));
  Residual = (ArcTan[Abs[Sinh[x]]]) - (ArcCos[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-177-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-177-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cos[x] != 0));
  Residual = (ArcTan[Abs[Tan[x]]]) - (Abs[ArcSin[Sin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-179-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-179-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= (Pi/2))) && ((Sinh[ArcCos[x]] != I)) && ((Sinh[ArcCos[x]] != (-I))) && ((Cosh[ArcCos[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCos[x]]]) - (ArcSin[Tanh[ArcCos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-179-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-179-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sinh[ArcCos[x]] != I)) && ((Sinh[ArcCos[x]] != (-I))) && ((Cosh[ArcCos[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCos[x]]]) - (ArcSin[Tanh[ArcCos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-180-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-180-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Sinh[ArcCosh[x]] != I)) && ((Sinh[ArcCosh[x]] != (-I))) && ((Cosh[ArcCosh[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCosh[x]]]) - (ArcSin[Tanh[ArcCosh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-180-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-180-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-180-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sinh[ArcCosh[x]] != I)) && ((Sinh[ArcCosh[x]] != (-I))) && ((Cosh[ArcCosh[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCosh[x]]]) - (ArcSin[Tanh[ArcCosh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-181-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-181-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= (Pi/2))) && ((Sinh[ArcSin[x]] != I)) && ((Sinh[ArcSin[x]] != (-I))) && ((Cosh[ArcSin[x]] != 0));
  Residual = (ArcTan[Sinh[ArcSin[x]]]) - (ArcSin[Tanh[ArcSin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-181-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-181-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sinh[ArcSin[x]] != I)) && ((Sinh[ArcSin[x]] != (-I))) && ((Cosh[ArcSin[x]] != 0));
  Residual = (ArcTan[Sinh[ArcSin[x]]]) - (ArcSin[Tanh[ArcSin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-183-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-183-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((Sinh[Log[x]] != I)) && ((Sinh[Log[x]] != (-I))) && ((Cosh[Log[x]] != 0));
  Residual = (ArcTan[Sinh[Log[x]]]) - (ArcSin[Tanh[Log[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-183-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-183-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && ((x != 0)) && ((Sinh[Log[x]] != I)) && ((Sinh[Log[x]] != (-I))) && ((Cosh[Log[x]] != 0));
  Residual = (ArcTan[Sinh[Log[x]]]) - (ArcSin[Tanh[Log[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-183-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-183-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Sinh[Log[x]] != I)) && ((Sinh[Log[x]] != (-I))) && ((Cosh[Log[x]] != 0));
  Residual = (ArcTan[Sinh[Log[x]]]) - (ArcSin[Tanh[Log[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-185-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-185-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[Cos[x]] != 0)) && ((Tan[Cos[x]] != I)) && ((Tan[Cos[x]] != (-I)));
  Residual = (ArcTan[Tan[Cos[x]]]) - (Cos[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-186-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-186-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cos[Sin[x]] != 0)) && ((Tan[Sin[x]] != I)) && ((Tan[Sin[x]] != (-I)));
  Residual = (ArcTan[Tan[Sin[x]]]) - (Sin[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-187-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-187-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0)) && ((Cos[Tanh[x]] != 0)) && ((Tan[Tanh[x]] != I)) && ((Tan[Tanh[x]] != (-I)));
  Residual = (ArcTan[Tan[Tanh[x]]]) - (Tanh[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-189-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-189-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cos[ArcSin[x]] != 1)) && ((Cos[ArcSin[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcSin[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-189-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-189-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcSin[x]] != 1)) && ((Cos[ArcSin[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcSin[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-190-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-190-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != I)) && ((x != (-I))) && ((Cos[ArcTan[x]] != 1)) && ((Cos[ArcTan[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcTan[x]]]) - (Abs[ArcSinh[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-190-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-190-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != I)) && ((x != (-I))) && ((Cos[ArcTan[x]] != 1)) && ((Cos[ArcTan[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcTan[x]]]) - (Abs[ArcSinh[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-190-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-190-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcTan[x]] != 1)) && ((Cos[ArcTan[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcTan[x]]]) - (Abs[ArcSinh[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-191-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-191-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Sin[ArcCos[x]] != 1)) && ((Sin[ArcCos[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Sin[ArcCos[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-191-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-191-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Sin[ArcCos[x]] != 1)) && ((Sin[ArcCos[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Sin[ArcCos[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-191-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-191-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sin[ArcCos[x]] != 1)) && ((Sin[ArcCos[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Sin[ArcCos[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-194-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-194-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sin[Cos[x]] != 1)) && ((Sin[Cos[x]] != (-1))) && ((Cos[Cos[x]] != 0));
  Residual = (ArcTanh[Sin[Cos[x]]]) - (ArcSinh[Tan[Cos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-195-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-195-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sin[Sin[x]] != 1)) && ((Sin[Sin[x]] != (-1))) && ((Cos[Sin[x]] != 0));
  Residual = (ArcTanh[Sin[Sin[x]]]) - (ArcSinh[Tan[Sin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-196-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-196-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0)) && ((Sin[Tanh[x]] != 1)) && ((Sin[Tanh[x]] != (-1))) && ((Cos[Tanh[x]] != 0));
  Residual = (ArcTanh[Sin[Tanh[x]]]) - (ArcSinh[Tan[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-196-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-196-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sin[Tanh[x]] != 1)) && ((Sin[Tanh[x]] != (-1))) && ((Cos[Tanh[x]] != 0));
  Residual = (ArcTanh[Sin[Tanh[x]]]) - (ArcSinh[Tan[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-20-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-20-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Sinh[Abs[x]]) - (Abs[Sinh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-20-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-20-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Sinh[Abs[x]]) - (Abs[Sinh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-200-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-200-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Cos[ArcSin[Sin[x]]]) - (Abs[Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-202-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-202-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cos[x] != 0)) && ((Tan[x] != I)) && ((Tan[x] != (-I)));
  Residual = (Cos[ArcTan[Tan[x]]]) - (Abs[Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-203-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-203-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((1/x) != 0));
  Residual = (Cos[Log[1/x]]) - (Cos[Log[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-203-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-203-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (Cos[Log[1/x]]) - (Cos[Log[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-203-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-203-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (Cos[Log[1/x]]) - (Cos[Log[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-205-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-205-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cos[x] != 0));
  Residual = (Cosh[ArcSinh[Tan[x]]]) - (Abs[1/Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-213-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-213-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((((-10)/x) != 0));
  Residual = (1/(-10/x)) - (x/-10);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-216-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-216-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((((-4)/x) != 0));
  Residual = (1/(-4/x)) - (x/-4);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-218-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-218-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((((-6)/x) != 0));
  Residual = (1/(-6/x)) - (x/-6);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-22-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-22-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0));
  Residual = (Tanh[Abs[x]]) - (Abs[Tanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-22-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-22-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Tanh[Abs[x]]) - (Abs[Tanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-220-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-220-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((((-8)/x) != 0));
  Residual = (1/(-8/x)) - (x/-8);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-229-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-229-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Power[Pi, x] != 0));
  Residual = (1/Pi^x) - ((1/Pi)^x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-233-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-233-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0)) && (((x != 0) || (Re[(-Pi)] > 0)));
  Residual = (1/x^Pi) - (x^(-Pi));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-234-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-234-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0)));
  Residual = (1/x^x) - ((1/x)^x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-234-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-234-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0)));
  Residual = (1/x^x) - ((1/x)^x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-234-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-234-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Integers]) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0)));
  Residual = (1/x^x) - ((1/x)^x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-234-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-234-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0)));
  Residual = (1/x^x) - ((1/x)^x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-241-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-241-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Surd[x, 3] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 3]]) - (Log[x]/3);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-243-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-243-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[x, Reals]) && ((Surd[x, 5] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 5]]) - (Log[x]/5);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-245-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-245-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[x, Reals]) && ((Surd[x, 7] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 7]]) - (Log[x]/7);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-247-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-247-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Surd[x, 9] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 9]]) - (Log[x]/9);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-248-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-248-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (-Abs[ArcSin[x]]) - (ArcSin[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-248-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-248-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (-Abs[ArcSin[x]]) - (ArcSin[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-249-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-249-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (-Abs[ArcSinh[x]]) - (ArcSinh[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-251-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-251-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((x != 1)) && ((x != (-1))) && (((-Abs[x]) != 1)) && (((-Abs[x]) != (-1)));
  Residual = (-Abs[ArcTanh[x]]) - (ArcTanh[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-251-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-251-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 1)) && ((x != (-1))) && (((-Abs[x]) != 1)) && (((-Abs[x]) != (-1)));
  Residual = (-Abs[ArcTanh[x]]) - (ArcTanh[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-252-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-252-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (-Abs[Sinh[x]]) - (Sinh[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-252-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-252-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (-Abs[Sinh[x]]) - (Sinh[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-253-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-253-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0));
  Residual = (-Abs[Tanh[x]]) - (Tanh[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-253-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-253-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (-Abs[Tanh[x]]) - (Tanh[-Abs[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-256-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-256-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((-Exp[x]) != 0));
  Residual = (-Exp[-x]) - (1/(-Exp[x]));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-260-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-260-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (-Log[Cos[x]]) - (Log[1/Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-260-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-260-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[Re[x]] < (Pi/2))) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (-Log[Cos[x]]) - (Log[1/Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-260-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-260-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (-Log[Cos[x]]) - (Log[1/Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-261-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-261-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0)) && (((1/Cosh[x]) != 0));
  Residual = (-Log[Cosh[x]]) - (Log[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-261-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-261-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && ((Cosh[x] != 0)) && (((1/Cosh[x]) != 0));
  Residual = (-Log[Cosh[x]]) - (Log[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-261-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-261-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cosh[x] != 0)) && (((1/Cosh[x]) != 0));
  Residual = (-Log[Cosh[x]]) - (Log[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-266-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-266-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((1/x) != 0));
  Residual = (-Sin[Log[x]]) - (Sin[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-266-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-266-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (-Sin[Log[x]]) - (Sin[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-266-condf · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-266-condf · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (-Sin[Log[x]]) - (Sin[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-266-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-266-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (-Sin[Log[x]]) - (Sin[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-267-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-267-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((Cos[Log[x]] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (-Tan[Log[x]]) - (Tan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-267-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-267-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && ((Cos[Log[x]] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (-Tan[Log[x]]) - (Tan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-267-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-267-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && ((Cos[Log[x]] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (-Tan[Log[x]]) - (Tan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-267-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-267-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cos[Log[x]] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (-Tan[Log[x]]) - (Tan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-274-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-274-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (Abs[x]^(-2)) - (x^(-2));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-275-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-275-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (Abs[x]^(-3)) - (Abs[x^(-3)]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-276-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-276-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (Abs[x]^(-4)) - (x^(-4));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-278-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-278-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (Abs[x]^(-6)) - (x^(-6));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-283-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-283-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Abs[x]^2) - (x*x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-283-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-283-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Abs[x]^2) - (x*x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-283-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-283-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Abs[x]^2) - (x*x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-284-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-284-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Abs[x]^3) - (Abs[x^3]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-286-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-286-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Abs[x]^5) - (Abs[x^5]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-287-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-287-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Abs[x]^6) - (x^6);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-288-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-288-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Abs[x]^7) - (Abs[x^7]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-289-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-289-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Abs[x]^8) - (x^8);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-289-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-289-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Abs[x]^8) - (x^8);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-29-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-29-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x != 0)) && ((Power[x, 3] != 0));
  Residual = (3*Log[x]) - (Log[x^3]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-29-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-29-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-29-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Power[x, 3] != 0));
  Residual = (3*Log[x]) - (Log[x^3]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-3-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-3-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcSinh[Sinh[x]]) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-30-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-30-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (4*Abs[x]) - (Abs[-4*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-31-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-31-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (5*Abs[x]) - (Abs[-5*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-326-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-326-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Exp[x]^2) - (Exp[2*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-33-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-33-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (6*Abs[x]) - (Abs[-6*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-334-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-334-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Exp[x] != 0) || (Re[Exp[1]] > 0)));
  Residual = (Exp[x]^Exp[1]) - (Exp[Exp[1]*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-334-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-334-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && (((Exp[x] != 0) || (Re[Exp[1]] > 0)));
  Residual = (Exp[x]^Exp[1]) - (Exp[Exp[1]*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-335-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-335-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Exp[x] != 0) || (Re[Pi] > 0)));
  Residual = (Exp[x]^Pi) - (Exp[Pi*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-335-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-335-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && (((Exp[x] != 0) || (Re[Pi] > 0)));
  Residual = (Exp[x]^Pi) - (Exp[Pi*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-336-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-336-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Exp[x] != 0) || (Re[x] > 0)));
  Residual = (Exp[x]^x) - (Exp[x*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-336-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-336-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && (((Exp[x] != 0) || (Re[x] > 0)));
  Residual = (Exp[x]^x) - (Exp[x*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-343-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-343-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = ((1/Pi)^x) - (Pi^(-x));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-343-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-343-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = ((1/Pi)^x) - (Pi^(-x));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-344-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-344-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-344-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-344-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-344-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-344-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-344-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-35-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-35-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Power[x, 7] != 0));
  Residual = (7*Log[x]) - (Log[x^7]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-354-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-354-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[Log[5]] > 0))) && ((x != 0));
  Residual = (x^Log[5]) - (5^Log[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-356-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-356-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[Log[7]] > 0))) && ((x != 0));
  Residual = (x^Log[7]) - (7^Log[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-359-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-359-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[Log[Pi]] > 0))) && ((x != 0));
  Residual = (x^Log[Pi]) - (Pi^Log[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-364-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-364-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Surd[Abs[x], 3]) - (Abs[Surd[x, 3]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-367-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-367-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Surd[Abs[x], 9]) - (Abs[Surd[x, 9]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-368-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-368-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (Element[ArcCos[x], Reals]) && ((ArcCos[x] != 0));
  Residual = (Surd[ArcCos[x], -5]) - (ArcCos[x]^(-5^(-1)));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-368-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-368-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[ArcCos[x], Reals]) && ((ArcCos[x] != 0));
  Residual = (Surd[ArcCos[x], -5]) - (ArcCos[x]^(-5^(-1)));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-369-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-369-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (Element[ArcCos[x], Reals]);
  Residual = (Surd[ArcCos[x], 5]) - (ArcCos[x]^(1/5));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-369-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-369-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[ArcCos[x], Reals]);
  Residual = (Surd[ArcCos[x], 5]) - (ArcCos[x]^(1/5));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-370-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-370-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (Element[ArcCosh[x], Reals]) && ((ArcCosh[x] != 0));
  Residual = (Surd[ArcCosh[x], -5]) - (ArcCosh[x]^(-5^(-1)));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-370-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-370-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[ArcCosh[x], Reals]) && ((ArcCosh[x] != 0));
  Residual = (Surd[ArcCosh[x], -5]) - (ArcCosh[x]^(-5^(-1)));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-371-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-371-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (Element[ArcCosh[x], Reals]);
  Residual = (Surd[ArcCosh[x], 5]) - (ArcCosh[x]^(1/5));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-371-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-371-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[ArcCosh[x], Reals]);
  Residual = (Surd[ArcCosh[x], 5]) - (ArcCosh[x]^(1/5));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-372-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-372-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (Element[Cosh[x], Reals]) && ((Cosh[x] != 0));
  Residual = (Surd[Cosh[x], -5]) - (Cosh[x]^(-5^(-1)));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-372-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-372-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[Cosh[x], Reals]) && ((Cosh[x] != 0));
  Residual = (Surd[Cosh[x], -5]) - (Cosh[x]^(-5^(-1)));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-372-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-372-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cosh[x] != 0));
  Residual = (Surd[Cosh[x], -5]) - (Cosh[x]^(-5^(-1)));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-373-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-373-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (Element[Cosh[x], Reals]);
  Residual = (Surd[Cosh[x], 5]) - (Cosh[x]^(1/5));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-373-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-373-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-373-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Surd[Cosh[x], 5]) - (Cosh[x]^(1/5));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-376-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-376-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[Im[x]] < Pi)) && (Element[Exp[x], Reals]) && ((Exp[x] != 0));
  Residual = (Surd[Exp[x], -3]) - (Exp[x/-3]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-378-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-378-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Exp[x] != 0));
  Residual = (Surd[Exp[x], -5]) - (Exp[x/-5]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-38-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-38-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Power[x, 9] != 0));
  Residual = (9*Log[x]) - (Log[x^9]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-380-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-380-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Exp[x] != 0));
  Residual = (Surd[Exp[x], -7]) - (Exp[x/-7]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-385-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-385-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[Exp[x], Reals]);
  Residual = (Surd[Exp[x], 3]) - (Exp[x/3]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-387-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-387-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (Element[Exp[x], Reals]);
  Residual = (Surd[Exp[x], 5]) - (Exp[x/5]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-389-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-389-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (Element[Exp[x], Reals]);
  Residual = (Surd[Exp[x], 7]) - (Exp[x/7]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-392-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-392-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (Sin[Abs[ArcSin[x]]]) - (Abs[Cos[ArcCos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-392-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-392-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sin[Abs[ArcSin[x]]]) - (Abs[Cos[ArcCos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-394-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-394-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((x != 1)) && ((x != (-1)));
  Residual = (Sin[Abs[ArcTanh[x]]]) - (Abs[Sin[ArcTanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-394-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-394-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 1)) && ((x != (-1)));
  Residual = (Sin[Abs[ArcTanh[x]]]) - (Abs[Sin[ArcTanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-395-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-395-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sin[Abs[Cos[x]]]) - (Abs[Sin[Cos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-396-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-396-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Sin[Abs[Sin[x]]]) - (Abs[Sin[Sin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-396-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-396-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sin[Abs[Sin[x]]]) - (Abs[Sin[Sin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-397-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-397-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sin[Abs[Tanh[x]]]) - (Abs[Sin[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-399-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-399-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Sin[ArcCos[Sin[x]]]) - (Abs[Cos[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-40-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-40-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Abs[x]*Pi) - (Abs[Pi*x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-402-cond · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-402-cond · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((Abs[x] != 1)) && ((x != 1)) && ((x != (-1)));
  Residual = (Sin[ArcTanh[Abs[x]]]) - (Abs[Sin[ArcTanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-402-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-402-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] != 1)) && ((x != 1)) && ((x != (-1)));
  Residual = (Sin[ArcTanh[Abs[x]]]) - (Abs[Sin[ArcTanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-403-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-403-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((1/x) != 0));
  Residual = (Sin[-Log[x]]) - (Sin[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-403-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-403-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (Sin[-Log[x]]) - (Sin[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-403-condf · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-403-condf · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (Sin[-Log[x]]) - (Sin[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-403-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-403-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (Sin[-Log[x]]) - (Sin[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-404-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-404-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0));
  Residual = (Sin[Tanh[Abs[x]]]) - (Abs[Sin[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-404-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-404-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sin[Tanh[Abs[x]]]) - (Abs[Sin[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-410-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-410-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Sinh[x] != 0));
  Residual = (Sinh[Exp[Log[x]]]) - (Exp[Log[Sinh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-412-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-412-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((Cos[Abs[ArcSin[x]]] != 0)) && ((Cos[ArcSin[x]] != 0));
  Residual = (Tan[Abs[ArcSin[x]]]) - (Abs[Tan[ArcSin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-412-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-412-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[Abs[ArcSin[x]]] != 0)) && ((Cos[ArcSin[x]] != 0));
  Residual = (Tan[Abs[ArcSin[x]]]) - (Abs[Tan[ArcSin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-413-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-413-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[Abs[Cos[x]]] != 0)) && ((Cos[Cos[x]] != 0));
  Residual = (Tan[Abs[Cos[x]]]) - (Abs[Tan[Cos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-414-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-414-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cos[Abs[Sin[x]]] != 0)) && ((Cos[Sin[x]] != 0));
  Residual = (Tan[Abs[Sin[x]]]) - (Abs[Tan[Sin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-414-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-414-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[Abs[Sin[x]]] != 0)) && ((Cos[Sin[x]] != 0));
  Residual = (Tan[Abs[Sin[x]]]) - (Abs[Tan[Sin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-415-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-415-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0)) && ((Cos[Abs[Tanh[x]]] != 0)) && ((Cos[Tanh[x]] != 0));
  Residual = (Tan[Abs[Tanh[x]]]) - (Abs[Tan[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-415-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-415-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[Abs[Tanh[x]]] != 0)) && ((Cos[Tanh[x]] != 0));
  Residual = (Tan[Abs[Tanh[x]]]) - (Abs[Tan[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-416-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-416-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1)) && ((Cos[ArcCos[Abs[x]]] != 0)) && ((Cos[ArcCos[x]] != 0));
  Residual = (Tan[ArcCos[Abs[x]]]) - (Abs[Tan[ArcCos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-416-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-416-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcCos[Abs[x]]] != 0)) && ((Cos[ArcCos[x]] != 0));
  Residual = (Tan[ArcCos[Abs[x]]]) - (Abs[Tan[ArcCos[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-417-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-417-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((Cos[ArcSin[Abs[x]]] != 0)) && ((Cos[ArcSin[x]] != 0));
  Residual = (Tan[ArcSin[Abs[x]]]) - (Abs[Tan[ArcSin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-417-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-417-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcSin[Abs[x]]] != 0)) && ((Cos[ArcSin[x]] != 0));
  Residual = (Tan[ArcSin[Abs[x]]]) - (Abs[Tan[ArcSin[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-420-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-420-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-420-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-420-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-420-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-420-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-420-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-421-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-421-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cos[Tanh[Abs[x]]] != 0)) && ((Cosh[x] != 0)) && ((Cos[Tanh[x]] != 0));
  Residual = (Tan[Tanh[Abs[x]]]) - (Abs[Tan[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-421-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-421-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[Tanh[Abs[x]]] != 0)) && ((Cos[Tanh[x]] != 0));
  Residual = (Tan[Tanh[Abs[x]]]) - (Abs[Tan[Tanh[x]]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-422-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-422-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Tanh[Abs[ArcSinh[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-422-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-422-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Tanh[Abs[ArcSinh[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-423-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-423-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[ArcCosh[Abs[x]]] != 0)) && ((x != 0));
  Residual = (Tanh[ArcCosh[Abs[x]]]) - (Cos[ArcSin[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-424-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-424-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Tanh[ArcSinh[Abs[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-424-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-428-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-428-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x <= 1));
  Residual = (ArcTan[Sinh[x]]) - (ArcSin[Tanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-428-cond3 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-428-cond3 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x >= 0)) && ((x <= Pi));
  Residual = (ArcTan[Sinh[x]]) - (ArcSin[Tanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-430-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-430-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0));
  Residual = (Log[x]*x) - (Log[x^x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-430-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-430-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x != 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0));
  Residual = (Log[x]*x) - (Log[x^x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-430-cond2 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-430-cond2 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((x != 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0));
  Residual = (Log[x]*x) - (Log[x^x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-430-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-430-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0));
  Residual = (Log[x]*x) - (Log[x^x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-432-cond3 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-432-cond3 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= (Pi/2))) && ((Cosh[x] != 0));
  Residual = (ArcCos[Abs[Tanh[x]]]) - (ArcSin[1/Cosh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-433-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-433-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((-Log[x]) != I)) && (((-Log[x]) != (-I))) && (((1/x) != 0)) && ((Log[(1/x)] != I)) && ((Log[(1/x)] != (-I)));
  Residual = (ArcTan[-Log[x]]) - (ArcTan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-433-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-433-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && (((-Log[x]) != I)) && (((-Log[x]) != (-I))) && (((1/x) != 0)) && ((Log[(1/x)] != I)) && ((Log[(1/x)] != (-I)));
  Residual = (ArcTan[-Log[x]]) - (ArcTan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-433-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-433-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && (((-Log[x]) != I)) && (((-Log[x]) != (-I))) && (((1/x) != 0)) && ((Log[(1/x)] != I)) && ((Log[(1/x)] != (-I)));
  Residual = (ArcTan[-Log[x]]) - (ArcTan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-433-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-433-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((-Log[x]) != I)) && (((-Log[x]) != (-I))) && (((1/x) != 0)) && ((Log[(1/x)] != I)) && ((Log[(1/x)] != (-I)));
  Residual = (ArcTan[-Log[x]]) - (ArcTan[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-442-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-442-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((Log[x] != 0)) && (((1/Log[x]) != 0));
  Residual = (-Log[Log[x]]) - (Log[1/Log[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-442-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-442-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && ((Log[x] != 0)) && (((1/Log[x]) != 0));
  Residual = (-Log[Log[x]]) - (Log[1/Log[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-442-cond4 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-442-cond4 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Integers]) && ((x != 0)) && ((Log[x] != 0)) && (((1/Log[x]) != 0));
  Residual = (-Log[Log[x]]) - (Log[1/Log[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-442-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-442-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Log[x] != 0)) && (((1/Log[x]) != 0));
  Residual = (-Log[Log[x]]) - (Log[1/Log[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-446-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-446-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != I)) && ((x != (-I))) && ((Cos[Abs[ArcTan[x]]] != 0));
  Residual = (Tan[Abs[ArcTan[x]]]) - (Abs[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-449-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-449-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cosh[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cosh[Log[(1/x)]] != 0));
  Residual = (Tanh[-Log[x]]) - (Tanh[Log[1/x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-450-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-450-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0));
  Residual = (x/x) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-450-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-450-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0));
  Residual = (x/x) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-451-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-451-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0));
  Residual = (0/x) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-451-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-451-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0));
  Residual = (0/x) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-46-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-46-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && ((Power[2, x] != 0));
  Residual = (Log[2]*x) - (Log[2^x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-5-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-5-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((Abs[x] != 1)) && ((x != 1)) && ((x != (-1)));
  Residual = (ArcTanh[Abs[x]]) - (Abs[ArcTanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-5-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-5-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] != 1)) && ((x != 1)) && ((x != (-1)));
  Residual = (ArcTanh[Abs[x]]) - (Abs[ArcTanh[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-50-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-50-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Power[6, x] != 0));
  Residual = (Log[6]*x) - (Log[6^x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-50-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-50-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Power[6, x] != 0));
  Residual = (Log[6]*x) - (Log[6^x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-51-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-51-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Power[7, x] != 0));
  Residual = (Log[7]*x) - (Log[7^x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-5372-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-5372-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Sin[ArcSin[1/-4]]) - (-4^(-1));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-5382-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-5382-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Sinh[Log[1/4]]) - (-15/8);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-5385-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-5385-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Sinh[-Log[4]]) - (-15/8);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-55-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-55-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((x != 0) || (Re[Exp[1]] > 0))) && ((Power[x, Exp[1]] != 0));
  Residual = (Log[x]*Exp[1]) - (Log[x^Exp[1]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-55-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-55-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x != 0)) && (((x != 0) || (Re[Exp[1]] > 0))) && ((Power[x, Exp[1]] != 0));
  Residual = (Log[x]*Exp[1]) - (Log[x^Exp[1]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-55-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-55-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[Exp[1]] > 0))) && ((Power[x, Exp[1]] != 0));
  Residual = (Log[x]*Exp[1]) - (Log[x^Exp[1]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-56-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-56-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((x != 0)) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0));
  Residual = (Log[x]*Pi) - (Log[x^Pi]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-56-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-56-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x != 0)) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0));
  Residual = (Log[x]*Pi) - (Log[x^Pi]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-56-condf · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-56-condf · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0));
  Residual = (Log[x]*Pi) - (Log[x^Pi]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-56-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-56-real · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0));
  Residual = (Log[x]*Pi) - (Log[x^Pi]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-6-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-6-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Cosh[x] != 0)) && ((Tanh[x] != 1)) && ((Tanh[x] != (-1)));
  Residual = (ArcTanh[Tanh[x]]) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-6-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-6-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Tanh[x] != 1)) && ((Tanh[x] != (-1)));
  Residual = (ArcTanh[Tanh[x]]) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-7-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-7-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (1/Abs[x]) - (Abs[1/x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-73-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-73-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] != 0)) && (((-Abs[x]) != 0));
  Residual = (-Abs[x]^(-1)) - (1/(-Abs[x]));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-80-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-80-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0)) && (((-Cos[x]) != 0));
  Residual = (-Cos[x]^(-1)) - (1/(-Cos[x]));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-806-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-806-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Cosh[0]) - (1);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-813-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-813-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Sinh[0]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-816-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-816-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Tanh[0]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-819-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-819-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0/Pi) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-83-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-83-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Log[x] != 0)) && (((-Log[x]) != 0));
  Residual = (-Log[x]^(-1)) - (1/(-Log[x]));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-837-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-837-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0^Pi) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-848-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-848-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Sinh[Log[4]]) - (15/8);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-86-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-86-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0)) && ((Tan[x] != 0)) && (((-Tan[x]) != 0));
  Residual = (-Tan[x]^(-1)) - (1/(-Tan[x]));
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-868-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-868-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0*ArcCosh[7]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-9-complex · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (declined correctly) *)
Print["== sp-acj4-9-complex · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Exp[x] != 0));
  Residual = (Log[Exp[x]]) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-192457 answered null (declined correctly)"];

(* ---- case sp-acj4-9-cond · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered null (no verdict) *)
Print["== sp-acj4-9-cond · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && ((Exp[x] != 0));
  Residual = (Log[Exp[x]]) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered null (no verdict)"];

(* ---- case sp-acj4-90-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-90-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (3/Abs[x]) - (Abs[-3/x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-90-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-90-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (3/Abs[x]) - (Abs[-3/x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-911-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-911-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0/ArcSin[-1]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-927-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-927-ground · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (0/ArcSinh[4]) - (0);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-94-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-94-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[x] != 0)) && ((x != 0));
  Residual = (7/Abs[x]) - (Abs[-7/x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-99-complex · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-99-complex · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]);
  Residual = (Abs[x]/3) - (Abs[x/-3]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];

(* ---- case sp-acj4-99-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-192457 answered true (solved) *)
Print["== sp-acj4-99-real · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Abs[x]/3) - (Abs[x/-3]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-192457 answered true (solved)"];
