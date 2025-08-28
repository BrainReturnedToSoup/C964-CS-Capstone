import d3 from "d3";
import type { Histogram_Interface } from "./interface";
import { useEffect, useRef } from "react";

function Histogram({
  width,
  height,
  margin,
  xAxisLabel,
  yAxisLabel,
  binWidth,
  data,
  style,
}: Histogram_Interface) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // clear any previous SVG thats there
    d3.select(containerRef.current).selectAll("*").remove();

    // Compute min, max, and bin thresholds
    const min = d3.min(data) as number;
    const max = d3.max(data) as number;
    const binThresholds = d3.range(min - binWidth, max + binWidth, binWidth);

    const bins = d3.bin().domain([min, max]).thresholds(binThresholds)(data);

    // Inner chart dimensions
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Scales
    const x = d3
      .scaleLinear()
      .domain([min - binWidth, max + binWidth])
      .range([0, innerWidth]);

    const yMax = d3.max(bins, (d) => d.length)!; // from the bins, find the bin with the max height, and use that as the yMax
    const y = d3
      .scaleLinear()
      .domain([0, yMax * 1.15]) // 15% buffer space to the top
      .range([innerHeight, 0]);

    // Create SVG
    const svg = d3
      .create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", style);

    // Group for margins
    const g = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Draw bars
    g.append("g")
      .attr("fill", "steelblue")
      .selectAll("rect")
      .data(bins)
      .join("rect")
      .attr("x", (d) => x(d.x0!))
      .attr("width", (d) => Math.max(0, x(d.x1!) - x(d.x0!) - 1)) // 1px gap
      .attr("y", (d) => y(d.length))
      .attr("height", (d) => innerHeight - y(d.length));

    // X-axis
    g.append("g")
      .attr("transform", `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).ticks(innerWidth / 50))
      .call((g) =>
        g
          .append("text")
          .attr("x", innerWidth)
          .attr("y", margin.bottom - 4)
          .attr("fill", "currentColor")
          .attr("text-anchor", "end")
          .text(xAxisLabel)
      );

    // Y-axis
    g.append("g")
      .call(d3.axisLeft(y).ticks(innerHeight / 20))
      .call((g) => g.select(".domain").remove())
      .call((g) =>
        g
          .append("text")
          .attr("x", -margin.left)
          .attr("y", 10)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text(yAxisLabel)
      );

    const containerRefInstance = containerRef.current;

    containerRefInstance.appendChild(svg.node()!);
  }, [margin, width, height, xAxisLabel, yAxisLabel, binWidth, data, style]);

  return (
    <>
      <div ref={containerRef}></div>
    </>
  );
}

export { Histogram };
