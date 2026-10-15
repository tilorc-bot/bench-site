(* assume-eval: suite examples · category branch-cuts · system wolfram-refine (5 cases listed) *)
(* 5 case run(s).  Global` is cleared before each, so no variable carries over; a failing case gives $Failed and the rest still run.  Run: wolframscript -file this-file.wls *)

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

(* ---- case demo-atan2-01 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261015-024442 answered true (solved) *)
Print["== demo-atan2-01 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[y, Reals]) && ((Element[x, Reals] && x > 0));
  Residual = (ArcTan[x, y]) - (ArcTan[y/x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261015-024442 answered true (solved)"];

(* ---- case demo-atan2-02 · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261015-024442 answered false (solved) *)
Print["== demo-atan2-02 · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[y, Reals]) && ((Element[x, Reals] && x < 0)) && ((Element[y, Reals] && y > 0));
  Residual = (ArcTan[x, y]) - (ArcTan[y/x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261015-024442 answered false (solved)"];

(* ---- case demo-log-01 · expected true · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261015-024442 answered null (no verdict) *)
Print["== demo-log-01 · wolfram-refine · expected true"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && (Element[y, Reals]) && ((Element[x, Reals] && x > 0)) && ((Element[y, Reals] && y > 0));
  Residual = (Log[x*y]) - (Log[x] + Log[y]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "true", "the run wolfram-refine-20261015-024442 answered null (no verdict)"];

(* ---- case demo-log-02 · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261015-024442 answered null (declined correctly) *)
Print["== demo-log-02 · wolfram-refine · expected contingent"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[z, Complexes]) && (Element[w, Complexes]) && ((z != 0)) && ((w != 0));
  Residual = (Log[z*w]) - (Log[z] + Log[w]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261015-024442 answered null (declined correctly)"];

(* ---- case demo-log-03 · expected false · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261015-024442 answered false (solved) *)
Print["== demo-log-03 · wolfram-refine · expected false"];
Quiet[Remove["Global`*"]];
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]) && ((Element[x, Reals] && x < 0));
  Residual = (Log[x]) - (Log[-x]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "false", "the run wolfram-refine-20261015-024442 answered false (solved)"];
