(* file: project4.ml
   author: Dr. Schwesinger
   semester: Fall, 2023
*)
open Printf

let parent (pid : int) (pr : Unix.file_descr) (pw : Unix.file_descr) : unit =

    (* convert file descriptors to channels *)
    let pr = Unix.in_channel_of_descr pr in
    let pw = Unix.out_channel_of_descr pw in

    (* initialize random number generator *)
    Unix.getpid () |> Random.init;
    let rand_int = (Random.int 98) + 1 in

    (* send random int to child *)
    printf "Parent sending to pipe: %d\n%!" rand_int;
    output_string pw ((string_of_int rand_int) ^ "\n");
    flush pw;

    (* send product int to child *)
    let product = rand_int * pid in
    printf "Parent sending to pipe: %d\n%!" product;
    output_string pw ((string_of_int product) ^ "\n");
    flush pw;

    (* receive result from child *)
    let result = input_line pr in
    printf "Parent received: %s\n%!" result;

    begin match result with
          | "Approved" -> printf "Parent: Thanks for playing!\n%!";
          | "Denied"   -> printf "Parent: Wrong, Please play again \n%!";
          | _ -> failwith "Got an incorrect response"
    end
    ;

    (* send BYE to child *)
    let msg = "BYE" in
    printf "Parent sending to pipe: %s\n%!" msg;
    output_string pw (msg ^ "\n");

    (* we are done so close channels *)
    close_in pr; close_out pw;

    (* wait for child to end *)
    let _ = Unix.wait () in ()


let child (cr : Unix.file_descr) (cw : Unix.file_descr) : unit =

    (* convert file descriptors to channels *)
    let cr = Unix.in_channel_of_descr cr in
    let cw = Unix.out_channel_of_descr cw in

    (* receive random int from parent *)
    let rand_int = int_of_string (input_line cr) in
    printf "Child received: %d\n%!" rand_int;

    (* receive random int from parent *)
    let product = int_of_string (input_line cr) in
    printf "Child received: %d\n%!" product;

    (* send result to parent *)
    let result = if (Unix.getpid ()) * rand_int = product
                 then "Approved"
                 else "Denied"
    in
    printf "Child sending to pipe: %s\n%!" result;
    output_string cw (result ^ "\n");
    flush cw;

    let response = input_line cr in
    printf "Child received: %s\n%!" response;

    match response with
    | "BYE" -> close_in cr; close_out cw
    | _ -> failwith "Did not get correct response from parent"


let () =
    try
        let cr, pw = Unix.pipe () in
        let pr, cw = Unix.pipe () in

        match Unix.fork () with
        | 0   -> Unix.close(pr); Unix.close(pw); child cr cw
        | pid -> Unix.close(cr); Unix.close(cw); parent pid pr pw

    with
    | Unix.Unix_error(_, fn, msg) -> printf "ERROR: %s, %s\n" fn msg
    | Failure msg -> printf "ERROR: %s\n" msg
