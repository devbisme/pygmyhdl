module tb_pwm_glitchless;

reg clk_i;
wire pwm_o;
reg [7:0] threshold;

initial begin
    $from_myhdl(
        clk_i,
        threshold
    );
    $to_myhdl(
        pwm_o
    );
end

pwm_glitchless dut(
    clk_i,
    pwm_o,
    threshold
);

endmodule
