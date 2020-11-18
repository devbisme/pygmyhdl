module tb_simpler_ram;

reg clk_i;
reg wr_i;
reg [7:0] addr_i;
reg [7:0] data_i;
wire [7:0] data_o;

initial begin
    $from_myhdl(
        clk_i,
        wr_i,
        addr_i,
        data_i
    );
    $to_myhdl(
        data_o
    );
end

simpler_ram dut(
    clk_i,
    wr_i,
    addr_i,
    data_i,
    data_o
);

endmodule
