(* assume-eval: suite simplipy · category simplipy-f64-edge · all Wolfram systems (45 cases listed) *)
(* 135 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case sp-acj4-0-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (no verdict) *)
Print["== sp-acj4-0-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCosh[Cosh[x]]) - (Abs[x]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered null (no verdict)"];

(* ---- case sp-acj4-0-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (no verdict) *)
Print["== sp-acj4-0-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCosh[Cosh[x]]) - (Abs[x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered null (no verdict)"];

(* ---- case sp-acj4-0-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered null (no verdict)"];

(* ---- case sp-acj4-115-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-115-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((x > 0)) && ((Surd[x, (-4)] != 0));
  Residual = (Log[x]/-4) - (Log[Surd[x, -4]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-115-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-115-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((x > 0)) && ((Surd[x, (-4)] != 0));
  Residual = (Log[x]/-4) - (Log[Surd[x, -4]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-115-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-116-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-116-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((x > 0)) && ((Surd[x, (-6)] != 0));
  Residual = (Log[x]/-6) - (Log[Surd[x, -6]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-116-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-116-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((x > 0)) && ((Surd[x, (-6)] != 0));
  Residual = (Log[x]/-6) - (Log[Surd[x, -6]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-116-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-130-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-130-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (Abs[Log[Cos[x]]]) - (Log[1/Cos[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-130-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-130-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (Abs[Log[Cos[x]]]) - (Log[1/Cos[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-130-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-151-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-151-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Cos[ArcSin[x]]]) - (Abs[ArcSin[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-151-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-151-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Cos[ArcSin[x]]]) - (Abs[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-151-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-154-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (no verdict) *)
Print["== sp-acj4-154-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Cos[Sin[x]]]) - (Abs[Sin[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered null (no verdict)"];

(* ---- case sp-acj4-154-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (no verdict) *)
Print["== sp-acj4-154-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Cos[Sin[x]]]) - (Abs[Sin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered null (no verdict)"];

(* ---- case sp-acj4-154-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered null (no verdict)"];

(* ---- case sp-acj4-156-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-156-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Sin[ArcCos[x]]]) - (Abs[ArcSin[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-156-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-156-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcCos[Sin[ArcCos[x]]]) - (Abs[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-156-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-180-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-180-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sinh[ArcCosh[x]] != I)) && ((Sinh[ArcCosh[x]] != (-I))) && ((Cosh[ArcCosh[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCosh[x]]]) - (ArcSin[Tanh[ArcCosh[x]]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-180-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-180-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sinh[ArcCosh[x]] != I)) && ((Sinh[ArcCosh[x]] != (-I))) && ((Cosh[ArcCosh[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCosh[x]]]) - (ArcSin[Tanh[ArcCosh[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-180-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-183-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-183-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Sinh[Log[x]] != I)) && ((Sinh[Log[x]] != (-I))) && ((Cosh[Log[x]] != 0));
  Residual = (ArcTan[Sinh[Log[x]]]) - (ArcSin[Tanh[Log[x]]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-183-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-183-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Sinh[Log[x]] != I)) && ((Sinh[Log[x]] != (-I))) && ((Cosh[Log[x]] != 0));
  Residual = (ArcTan[Sinh[Log[x]]]) - (ArcSin[Tanh[Log[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-183-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-189-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (no verdict) *)
Print["== sp-acj4-189-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcSin[x]] != 1)) && ((Cos[ArcSin[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcSin[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered null (no verdict)"];

(* ---- case sp-acj4-189-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (no verdict) *)
Print["== sp-acj4-189-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcSin[x]] != 1)) && ((Cos[ArcSin[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcSin[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered null (no verdict)"];

(* ---- case sp-acj4-189-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered null (no verdict)"];

(* ---- case sp-acj4-190-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (no verdict) *)
Print["== sp-acj4-190-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcTan[x]] != 1)) && ((Cos[ArcTan[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcTan[x]]]) - (Abs[ArcSinh[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered null (no verdict)"];

(* ---- case sp-acj4-190-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (no verdict) *)
Print["== sp-acj4-190-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcTan[x]] != 1)) && ((Cos[ArcTan[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcTan[x]]]) - (Abs[ArcSinh[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered null (no verdict)"];

(* ---- case sp-acj4-190-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered null (no verdict)"];

(* ---- case sp-acj4-191-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (no verdict) *)
Print["== sp-acj4-191-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sin[ArcCos[x]] != 1)) && ((Sin[ArcCos[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Sin[ArcCos[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered null (no verdict)"];

(* ---- case sp-acj4-191-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (no verdict) *)
Print["== sp-acj4-191-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Sin[ArcCos[x]] != 1)) && ((Sin[ArcCos[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Sin[ArcCos[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered null (no verdict)"];

(* ---- case sp-acj4-191-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered null (no verdict)"];

(* ---- case sp-acj4-203-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-203-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (Cos[Log[1/x]]) - (Cos[Log[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-203-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-203-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (Cos[Log[1/x]]) - (Cos[Log[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-203-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-229-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-229-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Power[Pi, x] != 0));
  Residual = (1/Pi^x) - ((1/Pi)^x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-229-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-229-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Power[Pi, x] != 0));
  Residual = (1/Pi^x) - ((1/Pi)^x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-229-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-234-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-234-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0)));
  Residual = (1/x^x) - ((1/x)^x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-234-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-234-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0)));
  Residual = (1/x^x) - ((1/x)^x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-234-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-241-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-241-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Surd[x, 3] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 3]]) - (Log[x]/3);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-241-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-241-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Surd[x, 3] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 3]]) - (Log[x]/3);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-241-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-247-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-247-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Surd[x, 9] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 9]]) - (Log[x]/9);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-247-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-247-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Surd[x, 9] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 9]]) - (Log[x]/9);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-247-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-260-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-260-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (-Log[Cos[x]]) - (Log[1/Cos[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-260-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-260-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (-Log[Cos[x]]) - (Log[1/Cos[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-260-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-261-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-261-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cosh[x] != 0)) && (((1/Cosh[x]) != 0));
  Residual = (-Log[Cosh[x]]) - (Log[1/Cosh[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-261-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (no verdict) *)
Print["== sp-acj4-261-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cosh[x] != 0)) && (((1/Cosh[x]) != 0));
  Residual = (-Log[Cosh[x]]) - (Log[1/Cosh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered null (no verdict)"];

(* ---- case sp-acj4-261-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-266-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-266-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (-Sin[Log[x]]) - (Sin[Log[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-266-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-266-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (-Sin[Log[x]]) - (Sin[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-266-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-267-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-267-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cos[Log[x]] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (-Tan[Log[x]]) - (Tan[Log[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-267-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-267-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cos[Log[x]] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (-Tan[Log[x]]) - (Tan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-267-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-29-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-29-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Power[x, 3] != 0));
  Residual = (3*Log[x]) - (Log[x^3]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-29-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-29-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Power[x, 3] != 0));
  Residual = (3*Log[x]) - (Log[x^3]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-29-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-3-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-3-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcSinh[Sinh[x]]) - (x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-3-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-3-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (ArcSinh[Sinh[x]]) - (x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-3-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-343-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-343-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = ((1/Pi)^x) - (Pi^(-x));
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-343-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-343-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = ((1/Pi)^x) - (Pi^(-x));
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-343-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-344-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-344-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-344-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-344-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-344-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-378-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-378-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Exp[x] != 0));
  Residual = (Surd[Exp[x], -5]) - (Exp[x/-5]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-378-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-378-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Exp[x] != 0));
  Residual = (Surd[Exp[x], -5]) - (Exp[x/-5]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-378-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-380-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-380-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Exp[x] != 0));
  Residual = (Surd[Exp[x], -7]) - (Exp[x/-7]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-380-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-380-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Exp[x] != 0));
  Residual = (Surd[Exp[x], -7]) - (Exp[x/-7]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-380-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-392-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-392-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sin[Abs[ArcSin[x]]]) - (Abs[Cos[ArcCos[x]]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-392-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-392-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sin[Abs[ArcSin[x]]]) - (Abs[Cos[ArcCos[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-392-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-403-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-403-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (Sin[-Log[x]]) - (Sin[Log[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-403-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-403-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((1/x) != 0));
  Residual = (Sin[-Log[x]]) - (Sin[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-403-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-410-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-410-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Sinh[x] != 0));
  Residual = (Sinh[Exp[Log[x]]]) - (Exp[Log[Sinh[x]]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-410-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-410-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Sinh[x] != 0));
  Residual = (Sinh[Exp[Log[x]]]) - (Exp[Log[Sinh[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-410-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-416-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-416-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcCos[Abs[x]]] != 0)) && ((Cos[ArcCos[x]] != 0));
  Residual = (Tan[ArcCos[Abs[x]]]) - (Abs[Tan[ArcCos[x]]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-416-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-416-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Cos[ArcCos[Abs[x]]] != 0)) && ((Cos[ArcCos[x]] != 0));
  Residual = (Tan[ArcCos[Abs[x]]]) - (Abs[Tan[ArcCos[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-416-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

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

(* ---- case sp-acj4-430-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-430-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0));
  Residual = (Log[x]*x) - (Log[x^x]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-430-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-430-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0));
  Residual = (Log[x]*x) - (Log[x^x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-430-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-433-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-433-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((-Log[x]) != I)) && (((-Log[x]) != (-I))) && (((1/x) != 0)) && ((Log[(1/x)] != I)) && ((Log[(1/x)] != (-I)));
  Residual = (ArcTan[-Log[x]]) - (ArcTan[Log[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-433-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-433-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((-Log[x]) != I)) && (((-Log[x]) != (-I))) && (((1/x) != 0)) && ((Log[(1/x)] != I)) && ((Log[(1/x)] != (-I)));
  Residual = (ArcTan[-Log[x]]) - (ArcTan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-433-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-442-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-442-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Log[x] != 0)) && (((1/Log[x]) != 0));
  Residual = (-Log[Log[x]]) - (Log[1/Log[x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-442-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-442-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Log[x] != 0)) && (((1/Log[x]) != 0));
  Residual = (-Log[Log[x]]) - (Log[1/Log[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-442-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-449-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-449-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cosh[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cosh[Log[(1/x)]] != 0));
  Residual = (Tanh[-Log[x]]) - (Tanh[Log[1/x]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-449-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (no verdict) *)
Print["== sp-acj4-449-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && ((Cosh[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cosh[Log[(1/x)]] != 0));
  Residual = (Tanh[-Log[x]]) - (Tanh[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered null (no verdict)"];

(* ---- case sp-acj4-449-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-450-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-450-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0));
  Residual = (x/x) - (1);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-450-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-450-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0));
  Residual = (x/x) - (1);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-450-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-451-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-451-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0));
  Residual = (0/x) - (0);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-451-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-451-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0));
  Residual = (0/x) - (0);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-451-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-50-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-50-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Power[6, x] != 0));
  Residual = (Log[6]*x) - (Log[6^x]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-50-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-50-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Power[6, x] != 0));
  Residual = (Log[6]*x) - (Log[6^x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-50-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-55-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-55-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[Exp[1]] > 0))) && ((Power[x, Exp[1]] != 0));
  Residual = (Log[x]*Exp[1]) - (Log[x^Exp[1]]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-55-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-55-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[Exp[1]] > 0))) && ((Power[x, Exp[1]] != 0));
  Residual = (Log[x]*Exp[1]) - (Log[x^Exp[1]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-55-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-56-real · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly) *)
Print["== sp-acj4-56-real · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0));
  Residual = (Log[x]*Pi) - (Log[x^Pi]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261018-213100 answered null (declined correctly)"];

(* ---- case sp-acj4-56-real · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered null (declined correctly) *)
Print["== sp-acj4-56-real · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x != 0)) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0));
  Residual = (Log[x]*Pi) - (Log[x^Pi]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261018-213049 answered null (declined correctly)"];

(* ---- case sp-acj4-56-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261018-213034 answered null (declined correctly)"];

(* ---- case sp-acj4-6-real · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-6-real · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Tanh[x] != 1)) && ((Tanh[x] != (-1)));
  Residual = (ArcTanh[Tanh[x]]) - (x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-6-real · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-6-real · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Tanh[x] != 1)) && ((Tanh[x] != (-1)));
  Residual = (ArcTanh[Tanh[x]]) - (x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-6-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-806-ground · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-806-ground · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Cosh[0]) - (1);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-806-ground · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-806-ground · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Cosh[0]) - (1);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-806-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-813-ground · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-813-ground · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Sinh[0]) - (0);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-813-ground · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-813-ground · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Sinh[0]) - (0);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-813-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];

(* ---- case sp-acj4-816-ground · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261018-213100 answered true (solved) *)
Print["== sp-acj4-816-ground · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Tanh[0]) - (0);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261018-213100 answered true (solved)"];

(* ---- case sp-acj4-816-ground · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261018-213049 answered true (solved) *)
Print["== sp-acj4-816-ground · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = True;
  Residual = (Tanh[0]) - (0);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261018-213049 answered true (solved)"];

(* ---- case sp-acj4-816-ground · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261018-213034 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261018-213034 answered true (solved)"];
