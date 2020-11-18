module tb_wax_wane;

reg clk_i;
wire led_o;

initial begin
    $from_myhdl(
        clk_i
    );
    $to_myhdl(
        led_o
    );
end

wax_wane dut(
    clk_i,
    led_o
);

endmodule
