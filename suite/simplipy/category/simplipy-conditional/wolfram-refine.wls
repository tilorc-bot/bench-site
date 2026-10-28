(* assume-eval: suite simplipy · category simplipy-conditional · system wolfram-refine (92 cases listed) *)
(* 92 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case sp-acj4-1-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-1-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (ArcSin[Abs[x]]) - (Abs[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-108-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-108-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && ((Abs[x] != 0));
  Residual = (Abs[x]/x) - (x/Abs[x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-124-condf · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-124-condf · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0));
  Residual = (Abs[ArcSin[Tanh[x]]]) - (ArcCos[1/Cosh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-127-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-127-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((Exp[x] != 1)) && ((Exp[x] != (-1)));
  Residual = (Abs[ArcTanh[Exp[x]]]) - (ArcTanh[Exp[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-128-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-128-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (Abs[Cos[ArcSin[x]]]) - (Cos[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-128-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-128-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x > 1));
  Residual = (Abs[Cos[ArcSin[x]]]) - (Cos[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-129-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-129-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != I)) && ((x != (-I)));
  Residual = (Abs[Cos[ArcTan[x]]]) - (Cos[ArcTan[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-130-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-130-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < (Pi/2))) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (Abs[Log[Cos[x]]]) - (Log[1/Cos[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-131-condf · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-131-condf · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0));
  Residual = (Abs[Log[Cosh[x]]]) - (Log[Cosh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-132-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-132-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x >= 0)) && ((x <= Pi)) && ((Sin[x] != 0));
  Residual = (Abs[Log[Sin[x]]]) - (-Log[Sin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-133-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-133-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0)) && ((Tanh[x] != 0));
  Residual = (Abs[Log[Tanh[x]]]) - (-Log[Tanh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-136-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-136-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x >= 0)) && (((x != 0) || (Re[Exp[1]] > 0)));
  Residual = (Abs[x^Exp[1]]) - (x^Exp[1]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-137-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-137-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x >= 0)) && (((x != 0) || (Re[Pi] > 0)));
  Residual = (Abs[x^Pi]) - (x^Pi);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-145-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-145-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (Abs[Sin[ArcCos[x]]]) - (Cos[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-145-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-145-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x > 1));
  Residual = (Abs[Sin[ArcCos[x]]]) - (Cos[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-147-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-147-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[ArcSinh[x]] != 0)) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Abs[Tanh[ArcSinh[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-151-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-151-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (ArcCos[Cos[ArcSin[x]]]) - (Abs[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-156-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-156-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (ArcCos[Sin[ArcCos[x]]]) - (Abs[ArcSin[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-159-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-159-cond3 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-159-cond3 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= (Pi/2))) && ((Cosh[x] != 0));
  Residual = (ArcCos[Tanh[Abs[x]]]) - (ArcSin[1/Cosh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-162-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-162-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && (Element[x, Reals]);
  Residual = (ArcCosh[Surd[x, 5]]) - (ArcCosh[x^(1/5)]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-162-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-162-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (ArcCosh[Surd[x, 5]]) - (ArcCosh[x^(1/5)]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-171-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-171-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[Im[x]] < Pi)) && ((Cosh[x] != 0));
  Residual = (ArcSin[Sin[Tanh[x]]]) - (Tanh[x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-171-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-171-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0));
  Residual = (ArcSin[Sin[Tanh[x]]]) - (Tanh[x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-179-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-179-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= (Pi/2))) && ((Sinh[ArcCos[x]] != I)) && ((Sinh[ArcCos[x]] != (-I))) && ((Cosh[ArcCos[x]] != 0));
  Residual = (ArcTan[Sinh[ArcCos[x]]]) - (ArcSin[Tanh[ArcCos[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-180-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-181-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-181-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= (Pi/2))) && ((Sinh[ArcSin[x]] != I)) && ((Sinh[ArcSin[x]] != (-I))) && ((Cosh[ArcSin[x]] != 0));
  Residual = (ArcTan[Sinh[ArcSin[x]]]) - (ArcSin[Tanh[ArcSin[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-183-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-183-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && ((x != 0)) && ((Sinh[Log[x]] != I)) && ((Sinh[Log[x]] != (-I))) && ((Cosh[Log[x]] != 0));
  Residual = (ArcTan[Sinh[Log[x]]]) - (ArcSin[Tanh[Log[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-186-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-186-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cos[Sin[x]] != 0)) && ((Tan[Sin[x]] != I)) && ((Tan[Sin[x]] != (-I)));
  Residual = (ArcTan[Tan[Sin[x]]]) - (Sin[x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-187-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-187-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0)) && ((Cos[Tanh[x]] != 0)) && ((Tan[Tanh[x]] != I)) && ((Tan[Tanh[x]] != (-I)));
  Residual = (ArcTan[Tan[Tanh[x]]]) - (Tanh[x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-190-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-190-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != I)) && ((x != (-I))) && ((Cos[ArcTan[x]] != 1)) && ((Cos[ArcTan[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Cos[ArcTan[x]]]) - (Abs[ArcSinh[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-191-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-191-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Sin[ArcCos[x]] != 1)) && ((Sin[ArcCos[x]] != (-1))) && ((x != 0));
  Residual = (ArcTanh[Sin[ArcCos[x]]]) - (ArcCosh[Abs[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-196-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-196-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cosh[x] != 0)) && ((Sin[Tanh[x]] != 1)) && ((Sin[Tanh[x]] != (-1))) && ((Cos[Tanh[x]] != 0));
  Residual = (ArcTanh[Sin[Tanh[x]]]) - (ArcSinh[Tan[Tanh[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-20-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-20-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Sinh[Abs[x]]) - (Abs[Sinh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-200-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-200-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Cos[ArcSin[Sin[x]]]) - (Abs[Cos[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-202-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-202-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cos[x] != 0)) && ((Tan[x] != I)) && ((Tan[x] != (-I)));
  Residual = (Cos[ArcTan[Tan[x]]]) - (Abs[Cos[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-203-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-203-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (Cos[Log[1/x]]) - (Cos[Log[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-205-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-205-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((Cos[x] != 0));
  Residual = (Cosh[ArcSinh[Tan[x]]]) - (Abs[1/Cos[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-234-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-234-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0)));
  Residual = (1/x^x) - ((1/x)^x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-234-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-234-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Integers]) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0)));
  Residual = (1/x^x) - ((1/x)^x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-243-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-243-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[x, Reals]) && ((Surd[x, 5] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 5]]) - (Log[x]/5);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-245-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-245-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[x, Reals]) && ((Surd[x, 7] != 0)) && ((x != 0));
  Residual = (Log[Surd[x, 7]]) - (Log[x]/7);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-248-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-248-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (-Abs[ArcSin[x]]) - (ArcSin[-Abs[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-251-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-251-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((x != 1)) && ((x != (-1))) && (((-Abs[x]) != 1)) && (((-Abs[x]) != (-1)));
  Residual = (-Abs[ArcTanh[x]]) - (ArcTanh[-Abs[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-260-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-260-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[Re[x]] < (Pi/2))) && ((Cos[x] != 0)) && (((1/Cos[x]) != 0));
  Residual = (-Log[Cos[x]]) - (Log[1/Cos[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-261-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-261-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && ((Cosh[x] != 0)) && (((1/Cosh[x]) != 0));
  Residual = (-Log[Cosh[x]]) - (Log[1/Cosh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-266-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-266-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (-Sin[Log[x]]) - (Sin[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-266-condf · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-266-condf · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (-Sin[Log[x]]) - (Sin[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-267-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-267-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && ((Cos[Log[x]] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (-Tan[Log[x]]) - (Tan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-267-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-267-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && ((Cos[Log[x]] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (-Tan[Log[x]]) - (Tan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-283-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-283-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Abs[x]^2) - (x*x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-287-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-287-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Abs[x]^6) - (x^6);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-289-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-289-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Abs[x]^8) - (x^8);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-29-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-29-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x != 0)) && ((Power[x, 3] != 0));
  Residual = (3*Log[x]) - (Log[x^3]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-29-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-334-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-334-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && (((Exp[x] != 0) || (Re[Exp[1]] > 0)));
  Residual = (Exp[x]^Exp[1]) - (Exp[Exp[1]*x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-335-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-335-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && (((Exp[x] != 0) || (Re[Pi] > 0)));
  Residual = (Exp[x]^Pi) - (Exp[Pi*x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-336-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-336-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && (((Exp[x] != 0) || (Re[x] > 0)));
  Residual = (Exp[x]^x) - (Exp[x*x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-344-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-344-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-344-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-344-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Integers]) && ((x != 0)) && ((((1/x) != 0) || (Re[x] > 0))) && (((x != 0) || (Re[(-x)] > 0)));
  Residual = ((1/x)^x) - (x^(-x));
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-372-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-372-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[Cosh[x], Reals]) && ((Cosh[x] != 0));
  Residual = (Surd[Cosh[x], -5]) - (Cosh[x]^(-5^(-1)));
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-373-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
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
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-376-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-376-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Abs[Im[x]] < Pi)) && (Element[Exp[x], Reals]) && ((Exp[x] != 0));
  Residual = (Surd[Exp[x], -3]) - (Exp[x/-3]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-385-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-385-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] > 0)) && (Element[Exp[x], Reals]);
  Residual = (Surd[Exp[x], 3]) - (Exp[x/3]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-392-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-392-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1));
  Residual = (Sin[Abs[ArcSin[x]]]) - (Abs[Cos[ArcCos[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-394-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-394-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((x != 1)) && ((x != (-1)));
  Residual = (Sin[Abs[ArcTanh[x]]]) - (Abs[Sin[ArcTanh[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-399-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-399-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0));
  Residual = (Sin[ArcCos[Sin[x]]]) - (Abs[Cos[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-402-cond · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-402-cond · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((Abs[x] != 1)) && ((x != 1)) && ((x != (-1)));
  Residual = (Sin[ArcTanh[Abs[x]]]) - (Abs[Sin[ArcTanh[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-403-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-403-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (Sin[-Log[x]]) - (Sin[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-403-condf · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (declined correctly) *)
Print["== sp-acj4-403-condf · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && (((1/x) != 0));
  Residual = (Sin[-Log[x]]) - (Sin[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261028-185652 answered null (declined correctly)"];

(* ---- case sp-acj4-412-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-412-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((Cos[Abs[ArcSin[x]]] != 0)) && ((Cos[ArcSin[x]] != 0));
  Residual = (Tan[Abs[ArcSin[x]]]) - (Abs[Tan[ArcSin[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-416-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-416-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= 1)) && ((Cos[ArcCos[Abs[x]]] != 0)) && ((Cos[ArcCos[x]] != 0));
  Residual = (Tan[ArcCos[Abs[x]]]) - (Abs[Tan[ArcCos[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-417-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-417-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((Cos[ArcSin[Abs[x]]] != 0)) && ((Cos[ArcSin[x]] != 0));
  Residual = (Tan[ArcSin[Abs[x]]]) - (Abs[Tan[ArcSin[x]]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-420-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-420-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-420-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-420-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-422-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-422-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && (((1/x) != I)) && (((1/x) != (-I)));
  Residual = (Tanh[Abs[ArcSinh[x]]]) - (Cos[ArcTan[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-424-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
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
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-428-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-428-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x <= 1));
  Residual = (ArcTan[Sinh[x]]) - (ArcSin[Tanh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-428-cond3 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-428-cond3 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((x >= 0)) && ((x <= Pi));
  Residual = (ArcTan[Sinh[x]]) - (ArcSin[Tanh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-430-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-430-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x != 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0));
  Residual = (Log[x]*x) - (Log[x^x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-430-cond2 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-430-cond2 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((x != 0)) && (((x != 0) || (Re[x] > 0))) && ((Power[x, x] != 0));
  Residual = (Log[x]*x) - (Log[x^x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-432-cond3 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-432-cond3 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] <= (Pi/2))) && ((Cosh[x] != 0));
  Residual = (ArcCos[Abs[Tanh[x]]]) - (ArcSin[1/Cosh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-433-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-433-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] >= 0)) && ((x != 0)) && (((-Log[x]) != I)) && (((-Log[x]) != (-I))) && (((1/x) != 0)) && ((Log[(1/x)] != I)) && ((Log[(1/x)] != (-I)));
  Residual = (ArcTan[-Log[x]]) - (ArcTan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-433-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-433-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0)) && ((x != 0)) && (((-Log[x]) != I)) && (((-Log[x]) != (-I))) && (((1/x) != 0)) && ((Log[(1/x)] != I)) && ((Log[(1/x)] != (-I)));
  Residual = (ArcTan[-Log[x]]) - (ArcTan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-442-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-442-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && ((Log[x] != 0)) && (((1/Log[x]) != 0));
  Residual = (-Log[Log[x]]) - (Log[1/Log[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-442-cond4 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-442-cond4 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Integers]) && ((x != 0)) && ((Log[x] != 0)) && (((1/Log[x]) != 0));
  Residual = (-Log[Log[x]]) - (Log[1/Log[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-46-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-46-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && ((Power[2, x] != 0));
  Residual = (Log[2]*x) - (Log[2^x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-5-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-5-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Abs[x] < 1)) && ((Abs[x] != 1)) && ((x != 1)) && ((x != (-1)));
  Residual = (ArcTanh[Abs[x]]) - (Abs[ArcTanh[x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-55-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-55-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x != 0)) && (((x != 0) || (Re[Exp[1]] > 0))) && ((Power[x, Exp[1]] != 0));
  Residual = (Log[x]*Exp[1]) - (Log[x^Exp[1]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-56-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered true (solved) *)
Print["== sp-acj4-56-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0)) && ((x != 0)) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0));
  Residual = (Log[x]*Pi) - (Log[x^Pi]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered true (solved)"];

(* ---- case sp-acj4-56-condf · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-56-condf · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && ((Re[x] == 0 && x != 0)) && ((x != 0)) && (((x != 0) || (Re[Pi] > 0))) && ((Power[x, Pi] != 0));
  Residual = (Log[x]*Pi) - (Log[x^Pi]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];

(* ---- case sp-acj4-9-cond · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261028-185652 answered null (no verdict) *)
Print["== sp-acj4-9-cond · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Complexes]) && (((Im[x] > (-Pi)) && (Im[x] <= Pi))) && ((Exp[x] != 0));
  Residual = (Log[Exp[x]]) - (x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261028-185652 answered null (no verdict)"];
