// Designer Agent - Diagram Generator
// Creates Mermaid diagrams and finalizes documentation

walker designer {
    has documentation;
    has code_graph;
    has final_docs = "";
    
    can generate_mermaid_diagram, embed_diagram_in_docs, save_documentation;
    
    des_node = spawn here node::designer;
    
    des_node {
        std.out("🎨 Designer: Creating diagrams...");
        
        // Generate Mermaid diagram from code graph
        mermaid_diagram = generate_mermaid_diagram(code_graph);
        std.out("🎨 Designer: Mermaid diagram generated");
        
        // Embed diagram into documentation
        final_docs = embed_diagram_in_docs(documentation, mermaid_diagram);
        
        // Save final documentation
        repo_name = extract_repo_name(code_graph);
        save_documentation(final_docs, repo_name);
        
        std.out("🎨 Designer: Documentation complete!");
        std.out("✅ Mission complete! Check outputs/" + repo_name + "/docs.md");
        
        // Return to Captain
        here.mission_result = {
            "status": "success",
            "repo_name": repo_name,
            "output_path": "outputs/" + repo_name + "/docs.md"
        };
    }
}

node designer (anchor des_anchor);

