module tb_ram;

reg clk_i;
reg wr_i;
reg [8:0] addr_i;
reg [23:0] data_i;
wire [23:0] data_o;

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

ram dut(
    clk_i,
    wr_i,
    addr_i,
    data_i,
    data_o
);

endmodule
