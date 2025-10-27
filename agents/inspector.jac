// Inspector Agent - Code Analyzer
// Parses code and builds Code Context Graph (CCG)

walker inspector {
    has repo_path;
    has file_tree;
    has readme_summary;
    has code_graph = {};
    
    can parse_code_structure, build_code_context_graph;
    
    insp_node = spawn here node::inspector;
    
    insp_node {
        std.out("🔍 Inspector: Analyzing code structure...");
        
        // Parse code files
        code_graph = build_code_context_graph(repo_path);
        
        if (code_graph != null):
            std.out("🔍 Inspector: Code Context Graph built");
            std.out("🔍 Inspector: Found " + code_graph.modules.length + " modules");
            std.out("🔍 Inspector: Found " + code_graph.nodes.length + " entities");
            
            // Move to Author
            spawn here walker::author(code_graph=code_graph, file_tree=file_tree, readme_summary=readme_summary);
        else:
            std.err("🔍 Inspector: Failed to analyze code");
    }
}

node inspector (anchor insp_anchor);

