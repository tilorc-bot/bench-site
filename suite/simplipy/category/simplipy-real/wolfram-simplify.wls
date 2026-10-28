(* assume-eval: suite simplipy · category simplipy-real · system wolfram-simplify (70 cases listed) *)
(* 70 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case sp-acj4-1-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-102-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-108-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-120-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-127-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-128-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-131-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-132-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-133-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-136-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-137-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-14-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-145-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-162-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-179-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-181-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-185-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-194-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-195-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-196-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-218-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-22-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-220-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-233-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-248-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-249-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-251-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-252-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-253-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-256-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-275-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-276-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-283-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-286-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-289-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-31-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-326-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-33-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-35-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-354-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-356-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-359-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-364-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-367-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-368-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-369-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-370-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-371-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-372-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-373-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-38-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-394-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-395-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-396-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-397-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-402-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-404-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-412-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-413-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-414-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-415-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-417-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-421-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered null (no verdict)"];

(* ---- case sp-acj4-5-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261028-001921 answered null (declined correctly)"];

(* ---- case sp-acj4-73-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-80-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-83-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-86-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-90-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];

(* ---- case sp-acj4-99-real · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261028-001921 answered true (solved) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261028-001921 answered true (solved)"];
