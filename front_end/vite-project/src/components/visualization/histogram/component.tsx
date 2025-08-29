import * as d3 from "d3";
import type { Histogram_Interface } from "./interface";
import { useEffect, useRef } from "react";

function Histogram({
  width,
  height,
  xAxisLabel,
  yAxisLabel,
  yNumOfTicks,
  xTickLabelInterval,
  binInterval,
  data,
  style,
}: Histogram_Interface) {
  const divRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!divRef.current) return;
    if (!data || data.length === 0) return;

    d3.select(divRef.current).selectAll("*").remove();

    const margin = { top: 80, left: 40, bottom: 40, right: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const [min, max] = d3.extent(data) as [number, number]; // min and max within the supplied data array
    const minBin = binInterval * Math.floor(min / binInterval); // finds the very left value representing bin
    const maxBin = binInterval * Math.ceil(max / binInterval) + binInterval; // finds the rightmost left value + an additional bin

    const binThresholds = d3.range(minBin, maxBin + binInterval, binInterval);

    const bins = d3
      .bin()
      .domain([minBin, maxBin + binInterval])
      .thresholds(binThresholds)(data);

    const xScale = d3
      .scaleLinear()
      .domain([
        minBin - (maxBin - minBin) * 0.03,
        maxBin + (maxBin - minBin) * 0.03,
      ])
      .range([0, innerWidth]);

    const yMax = d3.max(bins, (d) => d.length)!;
    const yScale = d3.scaleLinear().domain([0, yMax]).range([innerHeight, 0]);

    const svg = d3
      .create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", String(style));

    // Create a group for the chart area with margin translation
    const chartGroup = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Draw bars within the chart group (already margin-adjusted)
    chartGroup
      .append("g")
      .attr("fill", "steelblue")
      .selectAll("rect")
      .data(bins)
      .join("rect")
      .attr("x", (d) => xScale(d.x0 as number) + 1)
      .attr("width", (d) =>
        Math.max(0, xScale(d.x1 as number) - xScale(d.x0 as number) - 1)
      )
      .attr("y", (d) => yScale(d.length))
      .attr("height", (d) => innerHeight - yScale(d.length));

    // X-axis - position at bottom of chart area
    chartGroup
      .append("g")
      .attr("transform", `translate(0,${innerHeight})`)
      .call(
        d3.axisBottom(xScale).tickValues(
          binThresholds.filter((_, i) => i % xTickLabelInterval === 0) // Show every 2nd tick
        )
      )
      .call((g) =>
        g
          .append("text")
          .attr("x", innerWidth)
          .attr("y", margin.bottom - 4)
          .attr("fill", "currentColor")
          .attr("text-anchor", "end")
          .attr("font-weight", "bold")
          .attr("font-size", "0.85rem")
          .text(xAxisLabel)
      );

    // Y-axis - position at left of chart area
    chartGroup
      .append("g")
      .call(
        d3.axisLeft(yScale).ticks(yNumOfTicks).tickFormat(d3.format("d")) // Format as integers
      )
      .call((g) => g.select(".domain").remove())
      .call((g) =>
        g
          .append("text")
          .attr("x", 40) // Center in the left margin area
          .attr("y", -20) // Position above the top of the chart
          .attr("fill", "currentColor")
          .attr("text-anchor", "middle") // Center the text
          .attr("font-weight", "bold")
          .attr("font-size", "0.85rem")
          .text(yAxisLabel)
      );

    divRef.current.appendChild(svg.node()!);
  }, [
    width,
    height,
    xAxisLabel,
    yAxisLabel,
    yNumOfTicks,
    xTickLabelInterval,
    binInterval,
    data,
    style,
  ]);

  return <div ref={divRef} />;
}

export { Histogram };
