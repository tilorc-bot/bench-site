(* assume-eval: suite examples · category radicals · all Wolfram systems (6 cases listed) *)
(* 18 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case demo-eq-abs-01 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-040958 answered true (solved) *)
Print["== demo-eq-abs-01 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (Abs[x]) - (-x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261019-040958 answered true (solved)"];

(* ---- case demo-eq-abs-01 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-040953 answered true (solved) *)
Print["== demo-eq-abs-01 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (Abs[x]) - (-x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261019-040953 answered true (solved)"];

(* ---- case demo-eq-abs-01 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-040949 answered true (solved) *)
Print["== demo-eq-abs-01 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (Abs[x]) - (-x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261019-040949 answered true (solved)"];

(* ---- case demo-eq-abs-02 · expected false · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-040958 answered null (no verdict) *)
Print["== demo-eq-abs-02 · wolfram-fullsimplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (Abs[x]) - (x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-fullsimplify-20261019-040958 answered null (no verdict)"];

(* ---- case demo-eq-abs-02 · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-040953 answered null (no verdict) *)
Print["== demo-eq-abs-02 · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (Abs[x]) - (x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261019-040953 answered null (no verdict)"];

(* ---- case demo-eq-abs-02 · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-040949 answered null (no verdict) *)
Print["== demo-eq-abs-02 · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (Abs[x]) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261019-040949 answered null (no verdict)"];

(* ---- case demo-eq-sqrt-01 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-040958 answered true (solved) *)
Print["== demo-eq-sqrt-01 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0));
  Residual = (Sqrt[x^2]) - (x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261019-040958 answered true (solved)"];

(* ---- case demo-eq-sqrt-01 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-040953 answered true (solved) *)
Print["== demo-eq-sqrt-01 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0));
  Residual = (Sqrt[x^2]) - (x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261019-040953 answered true (solved)"];

(* ---- case demo-eq-sqrt-01 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-040949 answered true (solved) *)
Print["== demo-eq-sqrt-01 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0));
  Residual = (Sqrt[x^2]) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261019-040949 answered true (solved)"];

(* ---- case demo-eq-sqrt-02 · expected true · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-040958 answered true (solved) *)
Print["== demo-eq-sqrt-02 · wolfram-fullsimplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sqrt[x^2]) - (Abs[x]);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-fullsimplify-20261019-040958 answered true (solved)"];

(* ---- case demo-eq-sqrt-02 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-040953 answered true (solved) *)
Print["== demo-eq-sqrt-02 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sqrt[x^2]) - (Abs[x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261019-040953 answered true (solved)"];

(* ---- case demo-eq-sqrt-02 · expected true · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-040949 answered true (solved) *)
Print["== demo-eq-sqrt-02 · wolfram-simplify · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sqrt[x^2]) - (Abs[x]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-simplify-20261019-040949 answered true (solved)"];

(* ---- case demo-eq-sqrt-03 · expected contingent · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-040958 answered null (declined correctly) *)
Print["== demo-eq-sqrt-03 · wolfram-fullsimplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sqrt[x^2]) - (x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-fullsimplify-20261019-040958 answered null (declined correctly)"];

(* ---- case demo-eq-sqrt-03 · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-040953 answered null (declined correctly) *)
Print["== demo-eq-sqrt-03 · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sqrt[x^2]) - (x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261019-040953 answered null (declined correctly)"];

(* ---- case demo-eq-sqrt-03 · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-040949 answered null (declined correctly) *)
Print["== demo-eq-sqrt-03 · wolfram-simplify · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Sqrt[x^2]) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261019-040949 answered null (declined correctly)"];

(* ---- case demo-eq-sqrt-04 · expected false · system wolfram-fullsimplify (wolfram 14.3.0) *)
(* the run wolfram-fullsimplify-20261019-040958 answered false (solved) *)
Print["== demo-eq-sqrt-04 · wolfram-fullsimplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0));
  Residual = (Sqrt[x^2] + 1) - (x);
  Result = FullSimplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-fullsimplify-20261019-040958 answered false (solved)"];

(* ---- case demo-eq-sqrt-04 · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-040953 answered false (solved) *)
Print["== demo-eq-sqrt-04 · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0));
  Residual = (Sqrt[x^2] + 1) - (x);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261019-040953 answered false (solved)"];

(* ---- case demo-eq-sqrt-04 · expected false · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261019-040949 answered false (solved) *)
Print["== demo-eq-sqrt-04 · wolfram-simplify · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x > 0));
  Residual = (Sqrt[x^2] + 1) - (x);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-simplify-20261019-040949 answered false (solved)"];
