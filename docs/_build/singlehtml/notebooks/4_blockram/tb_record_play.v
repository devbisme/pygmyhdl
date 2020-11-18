module tb_record_play;

reg clk_i;
reg button_a;
reg button_b;
wire [4:0] leds_o;

initial begin
    $from_myhdl(
        clk_i,
        button_a,
        button_b
    );
    $to_myhdl(
        leds_o
    );
end

record_play dut(
    clk_i,
    button_a,
    button_b,
    leds_o
);

endmodule
