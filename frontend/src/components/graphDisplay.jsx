import React from "react";
import { Graph } from "react-d3-graph";

function GraphDisplay({ graphData }) {
  if (!graphData) return null;

  const data = {
    nodes: graphData.nodes,
    links: graphData.links,
  };

  const config = {
    nodeHighlightBehavior: true,
    node: {
      color: "lightblue",
      size: 120,
      highlightStrokeColor: "blue",
    },
    link: {
      highlightColor: "lightblue",
    },
  };

  const onClickNode = function (nodeId) {
    console.log(`Clicked node ${nodeId}`);
  };

  return (
    <div className="graph-container">
      <Graph
        id="fact-check-graph"
        data={data}
        config={config}
        onClickNode={onClickNode}
      />
    </div>
  );
}

export default GraphDisplay;
