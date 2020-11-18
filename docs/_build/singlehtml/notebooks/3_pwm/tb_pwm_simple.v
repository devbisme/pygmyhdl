module tb_pwm_simple;

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

pwm_simple dut(
    clk_i,
    pwm_o,
    threshold
);

endmodule
