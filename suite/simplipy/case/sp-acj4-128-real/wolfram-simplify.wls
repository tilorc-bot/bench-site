(* assume-eval: case sp-acj4-128-real · expected contingent · system wolfram-simplify (wolfram 14.3.0) *)
(* the run wolfram-simplify-20261015-025035 answered null (declined correctly) *)
(* Run: wolframscript -file this-file.wls.  The harness's setup only warms up the kernel and silences messages: left out. *)

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

(* the query code, exactly as it ran, evaluated as the adapter does *)
AEScript`out = Quiet[Check[
(
  Assum = (Element[x, Reals]);
  Residual = (Abs[Cos[ArcSin[x]]]) - (Cos[ArcSin[x]]);
  Result = Simplify[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-simplify-20261015-025035 answered null (declined correctly)"];
