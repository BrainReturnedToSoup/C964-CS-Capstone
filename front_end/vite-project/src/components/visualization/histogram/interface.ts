interface Margin {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

type Data = number[];

export interface Histogram_Interface {
  width: number;
  height: number;
  margin: Margin;
  xAxisLabel: string;
  yAxisLabel: string;
  binWidth: number;
  data: Data; 
  style: string;
}
