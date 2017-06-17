module tb_and_g;

reg a;
reg b;
wire c;

initial begin
    $from_myhdl(
        a,
        b
    );
    $to_myhdl(
        c
    );
end

and_g dut(
    a,
    b,
    c
);

endmodule
