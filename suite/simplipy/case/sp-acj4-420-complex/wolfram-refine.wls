(* assume-eval: case sp-acj4-420-complex · expected contingent · system wolfram-refine (wolfram 14.3.0) *)
(* the run wolfram-refine-20261019-184729 answered null (declined correctly) *)
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
  Assum = (Element[x, Complexes]) && ((x != 0)) && ((Cos[(-Log[x])] != 0)) && (((1/x) != 0)) && ((Cos[Log[(1/x)]] != 0));
  Residual = (Tan[-Log[x]]) - (Tan[Log[1/x]]);
  Result = Refine[Residual, Assum];
  Answer = Which[Result === 0, True, NumericQ[Result] && TrueQ[Result != 0], False, True, Null];
  {Residual, Result, Answer}
)
, $Failed]];
AEScript`verdict[AEScript`out, "contingent", "the run wolfram-refine-20261019-184729 answered null (declined correctly)"];
