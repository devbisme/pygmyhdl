module tb_and3_g;

reg a;
reg b;
reg c;
wire o;

initial begin
    $from_myhdl(
        a,
        b,
        c
    );
    $to_myhdl(
        o
    );
end

and3_g dut(
    a,
    b,
    c,
    o
);

endmodule
