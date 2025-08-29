type Data = number[];

export interface Histogram_Interface {
  width: number;
  height: number;
  xAxisLabel: string;
  yAxisLabel: string;
  yNumOfTicks: number;
  xTickLabelInterval: number;
  binInterval: number;
  data: Data;
  style: React.CSSProperties;
}
