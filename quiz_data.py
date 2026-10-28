"""
quiz_data.py
============
Contains the comprehensive question bank for the Python Quiz Application.
Includes 5 categories with 15 questions each (5 Easy, 5 Medium, 5 Hard)
totalling 75 questions. Each question contains 4 options, the correct
answer index, and a comprehensive explanation.
"""

CATEGORIES = [
    "Python Programming",
    "C++ Programming",
    "Data Structures",
    "Artificial Intelligence and Machine Learning",
    "General Knowledge"
]

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

# Time allowed per question in seconds based on difficulty
TIME_PER_QUESTION = {
    "Easy": 45,
    "Medium": 30,
    "Hard": 25,
    "All": 35
}

QUESTIONS_DATA = [
    # =========================================================================
    # 1. PYTHON PROGRAMMING (15 Questions: 5 Easy, 5 Medium, 5 Hard)
    # =========================================================================
    {
        "id": 1,
        "category": "Python Programming",
        "difficulty": "Easy",
        "question": "What is the correct file extension for Python script files?",
        "options": [".pyth", ".pt", ".py", ".pyt"],
        "correct_index": 2,
        "explanation": "Python source files use the '.py' extension, which is recognized by the Python interpreter and modern code editors."
    },
    {
        "id": 2,
        "category": "Python Programming",
        "difficulty": "Easy",
        "question": "Which keyword is used to create a function in Python?",
        "options": ["function", "def", "fun", "define"],
        "correct_index": 1,
        "explanation": "In Python, the 'def' keyword (short for 'define') is used to declare user-defined functions."
    },
    {
        "id": 3,
        "category": "Python Programming",
        "difficulty": "Easy",
        "question": "Which of the following data types in Python is IMMUTABLE?",
        "options": ["List", "Dictionary", "Set", "Tuple"],
        "correct_index": 3,
        "explanation": "Tuples cannot be modified after creation (immutable), whereas lists, dictionaries, and sets are mutable."
    },
    {
        "id": 4,
        "category": "Python Programming",
        "difficulty": "Easy",
        "question": "What will be the output of: print(type(5 / 2)) in Python 3?",
        "options": ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'number'>"],
        "correct_index": 1,
        "explanation": "In Python 3, the single slash '/' performs true division and always yields a float (e.g., 5 / 2 = 2.5)."
    },
    {
        "id": 5,
        "category": "Python Programming",
        "difficulty": "Easy",
        "question": "Which built-in function returns the total number of items in an object?",
        "options": ["count()", "size()", "len()", "length()"],
        "correct_index": 2,
        "explanation": "The len() function returns the number of items in a sequence (string, list, tuple) or collection (dictionary, set)."
    },
    {
        "id": 6,
        "category": "Python Programming",
        "difficulty": "Medium",
        "question": "What does the *args parameter syntax allow a function to accept?",
        "options": [
            "Any number of keyword arguments",
            "Any number of positional arguments as a tuple",
            "A pointer to another function",
            "A mandatory dictionary of arguments"
        ],
        "correct_index": 1,
        "explanation": "*args allows a function to accept an arbitrary number of positional arguments, packed into a single tuple."
    },
    {
        "id": 7,
        "category": "Python Programming",
        "difficulty": "Medium",
        "question": "What is the output of the list comprehension: [x**2 for x in range(5) if x % 2 == 1]?",
        "options": ["[1, 9]", "[0, 4, 16]", "[1, 4, 9]", "[1, 9, 25]"],
        "correct_index": 0,
        "explanation": "range(5) produces [0, 1, 2, 3, 4]. The odd numbers are 1 and 3. Their squares are 1**2 = 1 and 3**2 = 9."
    },
    {
        "id": 8,
        "category": "Python Programming",
        "difficulty": "Medium",
        "question": "How does the 'is' operator differ from the '==' operator in Python?",
        "options": [
            "'is' compares object identity (memory address); '==' compares values for equality",
            "'==' compares object identity; 'is' compares values",
            "'is' works only with strings; '==' works with numbers",
            "There is no difference; they are aliases"
        ],
        "correct_index": 0,
        "explanation": "'==' checks whether the values of two objects are equal, while 'is' checks whether both references point to the exact same memory address (id)."
    },
    {
        "id": 9,
        "category": "Python Programming",
        "difficulty": "Medium",
        "question": "Which Python module is part of the standard library for interacting with SQLite databases?",
        "options": ["sqlpython", "pysql", "sqlite3", "dbsqlite"],
        "correct_index": 2,
        "explanation": "The 'sqlite3' module provides a DB-API 2.0 compliant interface to SQLite and is built into Python's standard library."
    },
    {
        "id": 10,
        "category": "Python Programming",
        "difficulty": "Medium",
        "question": "What does a Python decorator fundamentally do?",
        "options": [
            "Styles the graphical user interface of an app",
            "Takes a function as argument and extends its behavior without modifying it",
            "Compresses bytecode to speed up execution",
            "Converts procedural code into object-oriented classes"
        ],
        "correct_index": 1,
        "explanation": "A decorator is a callable that takes another function as an argument, wraps it to extend its behavior, and returns the modified function."
    },
    {
        "id": 11,
        "category": "Python Programming",
        "difficulty": "Hard",
        "question": "What is the purpose of Python's Global Interpreter Lock (GIL)?",
        "options": [
            "It speeds up multi-threaded CPU-bound programs across multiple cores",
            "It synchronizes the execution of threads so only one native thread executes Python bytecode at a time",
            "It encrypts Python bytecode during network transfers",
            "It prevents unauthorized users from inspecting script variables"
        ],
        "correct_index": 1,
        "explanation": "The GIL is a mutex that prevents multiple native OS threads from executing Python bytecodes concurrently, primarily protecting CPython's memory management."
    },
    {
        "id": 12,
        "category": "Python Programming",
        "difficulty": "Hard",
        "question": "What is the difference between a generator and an ordinary list in terms of memory?",
        "options": [
            "Generators store all items in RAM at once; lists load them lazily",
            "Generators yield items one by one on-demand (lazy evaluation), consuming O(1) auxiliary memory",
            "Generators are stored on disk; lists are kept in CPU L1 cache",
            "Lists can only store numbers while generators can store any type"
        ],
        "correct_index": 1,
        "explanation": "Generators produce items dynamically using the 'yield' keyword without materializing the whole sequence in memory, keeping space complexity to O(1)."
    },
    {
        "id": 13,
        "category": "Python Programming",
        "difficulty": "Hard",
        "question": "In Python metaclasses, which method is responsible for ALLOCATING a new class instance before __init__ is called?",
        "options": ["__alloc__", "__new__", "__prepare__", "__construct__"],
        "correct_index": 1,
        "explanation": "__new__ is the actual constructor method that allocates memory and returns a new object instance, which is then initialized by __init__."
    },
    {
        "id": 14,
        "category": "Python Programming",
        "difficulty": "Hard",
        "question": "What is the Method Resolution Order (MRO) algorithm used by Python 3 for multiple inheritance?",
        "options": ["Depth-First Search (DFS)", "Breadth-First Search (BFS)", "C3 Linearization Algorithm", "Dijkstra MRO"],
        "correct_index": 2,
        "explanation": "Python 2.3+ and Python 3 use the C3 Linearization algorithm to compute a deterministic MRO that respects local precedence and monotonicity."
    },
    {
        "id": 15,
        "category": "Python Programming",
        "difficulty": "Hard",
        "question": "What does the '__slots__' declaration in a Python class accomplish?",
        "options": [
            "Restricts attribute creation to a predefined set and eliminates the per-instance __dict__, saving memory",
            "Enables multithreading locks on every instance attribute",
            "Automatically serializes instances into JSON format",
            "Provides hardware GPU acceleration for numerical attributes"
        ],
        "correct_index": 0,
        "explanation": "__slots__ tells Python not to use an open dictionary for each instance, substantially reducing RAM overhead for classes instantiated millions of times."
    },

    # =========================================================================
    # 2. C++ PROGRAMMING (15 Questions: 5 Easy, 5 Medium, 5 Hard)
    # =========================================================================
    {
        "id": 16,
        "category": "C++ Programming",
        "difficulty": "Easy",
        "question": "Who created the C++ programming language?",
        "options": ["Dennis Ritchie", "Bjarne Stroustrup", "James Gosling", "Guido van Rossum"],
        "correct_index": 1,
        "explanation": "Bjarne Stroustrup developed C++ at Bell Laboratories in 1979 as an extension of the C language with classes."
    },
    {
        "id": 17,
        "category": "C++ Programming",
        "difficulty": "Easy",
        "question": "Which stream object is used for standard console output in C++?",
        "options": ["cin", "cout", "cerr", "print"],
        "correct_index": 1,
        "explanation": "std::cout (character output) in the <iostream> header is used to send formatted data to the standard output device (console)."
    },
    {
        "id": 18,
        "category": "C++ Programming",
        "difficulty": "Easy",
        "question": "Which operator is used to access members of a structure or class through a POINTER in C++?",
        "options": [". (dot)", ":: (scope resolution)", "-> (arrow)", "* (dereference)"],
        "correct_index": 2,
        "explanation": "The arrow operator '->' is syntactic sugar for dereferencing a pointer and accessing a member: (*ptr).member."
    },
    {
        "id": 19,
        "category": "C++ Programming",
        "difficulty": "Easy",
        "question": "What is the default access specifier for members of a 'class' in C++?",
        "options": ["public", "protected", "private", "internal"],
        "correct_index": 2,
        "explanation": "In C++, members of a 'class' default to 'private', whereas members of a 'struct' default to 'public'."
    },
    {
        "id": 20,
        "category": "C++ Programming",
        "difficulty": "Easy",
        "question": "Which header file is required to use dynamic arrays represented by std::vector?",
        "options": ["<array>", "<vector>", "<list>", "<dynamic>"],
        "correct_index": 1,
        "explanation": "The <vector> standard header contains the template definition for std::vector, a contiguous dynamic array container."
    },
    {
        "id": 21,
        "category": "C++ Programming",
        "difficulty": "Medium",
        "question": "What keyword is placed before a base class member function to achieve run-time polymorphism in C++?",
        "options": ["dynamic", "inline", "virtual", "override"],
        "correct_index": 2,
        "explanation": "The 'virtual' keyword instructs the compiler to generate a vtable entry, enabling late binding and dynamic dispatch based on actual runtime object type."
    },
    {
        "id": 22,
        "category": "C++ Programming",
        "difficulty": "Medium",
        "question": "What is a 'pure virtual function' in C++?",
        "options": [
            "A function that executes in constant time O(1)",
            "A virtual function declared with '= 0' that must be overridden by concrete derived classes",
            "A static member function that takes no parameters",
            "A function without any side effects"
        ],
        "correct_index": 1,
        "explanation": "A pure virtual function is declared as 'virtual void func() = 0;' in an abstract class and has no base implementation, making the class uninstantiable."
    },
    {
        "id": 23,
        "category": "C++ Programming",
        "difficulty": "Medium",
        "question": "Which smart pointer in modern C++ (C++11) represents EXCLUSIVE ownership of a dynamically allocated object?",
        "options": ["std::shared_ptr", "std::weak_ptr", "std::unique_ptr", "std::auto_ptr"],
        "correct_index": 2,
        "explanation": "std::unique_ptr owns and manages an object exclusively; it cannot be copied, only moved, guaranteeing zero-overhead single ownership."
    },
    {
        "id": 24,
        "category": "C++ Programming",
        "difficulty": "Medium",
        "question": "What problem does the 'diamond problem' in C++ multiple inheritance cause, and how is it solved?",
        "options": [
            "Stack overflow; solved using recursion depth limits",
            "Ambiguity and duplicate base subobjects; solved using 'virtual inheritance'",
            "Compilation slowdown; solved using precompiled headers",
            "Memory leaks; solved using garbage collection"
        ],
        "correct_index": 1,
        "explanation": "When two derived classes share a base class and another class inherits from both, duplicate base instances occur. 'virtual base class' ensures only one shared instance."
    },
    {
        "id": 25,
        "category": "C++ Programming",
        "difficulty": "Medium",
        "question": "What does the RAII (Resource Acquisition Is Initialization) idiom mean in C++?",
        "options": [
            "Variables must always be assigned 0 when declared",
            "Resources (memory, file handles) are bound to object lifetime; acquired in constructor, released in destructor",
            "All classes must be defined inside standard templates",
            "Compiler optimizes away all constructors"
        ],
        "correct_index": 1,
        "explanation": "RAII ties resource lifecycle to object scope. The destructor is deterministically invoked when an object leaves scope, preventing memory/resource leaks."
    },
    {
        "id": 26,
        "category": "C++ Programming",
        "difficulty": "Hard",
        "question": "What is 'move semantics' in C++11, and which reference type enables it?",
        "options": [
            "Copying byte-by-byte using memcpy; enabled by const references",
            "Stealing internal resources from temporary objects instead of deep-copying; enabled by rvalue references (T&&)",
            "Relocating executables in RAM; enabled by void* pointers",
            "Converting C++ objects to JSON; enabled by auto"
        ],
        "correct_index": 1,
        "explanation": "Move semantics allows transferring ownership of heap buffers from temporary/dying objects (rvalues) using rvalue references (&&) without expensive allocations."
    },
    {
        "id": 27,
        "category": "C++ Programming",
        "difficulty": "Hard",
        "question": "What does SFINAE stand for in template metaprogramming?",
        "options": [
            "Static Function Invocation Never Alters Execution",
            "Substitution Failure Is Not An Error",
            "Sequential Fast Iteration Naturally Avoids Errors",
            "Syntax Formatting Is Never Automatically Enforced"
        ],
        "correct_index": 1,
        "explanation": "'Substitution Failure Is Not An Error' means if a template substitution error occurs while evaluating function overloads, the candidate is discarded without failing compilation."
    },
    {
        "id": 28,
        "category": "C++ Programming",
        "difficulty": "Hard",
        "question": "What is the purpose of 'std::memory_order_acquire' and 'std::memory_order_release' in C++ atomic operations?",
        "options": [
            "Allocating and freeing dynamic RAM",
            "Ensuring synchronized memory visibility across threads without full global memory fences",
            "Preventing heap fragmentation in standard vectors",
            "Locking GUI window threads during rendering"
        ],
        "correct_index": 1,
        "explanation": "Acquire-release semantics enforce ordering constraints on memory operations across concurrent threads, ensuring writes in release threads are visible after acquire."
    },
    {
        "id": 29,
        "category": "C++ Programming",
        "difficulty": "Hard",
        "question": "Why should a base class destructor almost always be declared as 'virtual' when polymorphic deletion is expected?",
        "options": [
            "To allow the constructor to run in reverse",
            "To prevent undefined behavior and ensure the derived class destructor is invoked when deleting via a base pointer",
            "To make destructors accessible outside the namespace",
            "It is required by the C++ standard for every class"
        ],
        "correct_index": 1,
        "explanation": "Deleting a derived object through a base pointer with a non-virtual destructor results in undefined behavior and skips the derived class destructor, causing resource leaks."
    },
    {
        "id": 30,
        "category": "C++ Programming",
        "difficulty": "Hard",
        "question": "What does 'constexpr' guarantee in modern C++ (C++11/C++14/C++20)?",
        "options": [
            "The variable or function is evaluated at COMPILE TIME whenever its arguments are constant expressions",
            "The variable is strictly read-only at runtime in ROM",
            "The function can never throw any runtime exceptions",
            "The function runs inside an isolated CPU sandbox"
        ],
        "correct_index": 0,
        "explanation": "'constexpr' specifies that the value of an object or return value of a function can be evaluated at compile time, improving runtime performance."
    },

    # =========================================================================
    # 3. DATA STRUCTURES (15 Questions: 5 Easy, 5 Medium, 5 Hard)
    # =========================================================================
    {
        "id": 31,
        "category": "Data Structures",
        "difficulty": "Easy",
        "question": "Which principle does a Stack data structure follow?",
        "options": ["First In First Out (FIFO)", "Last In First Out (LIFO)", "First In Never Out (FINO)", "Priority Based Ordering"],
        "correct_index": 1,
        "explanation": "A stack operates on LIFO (Last In First Out), where the element inserted most recently is the first one removed."
    },
    {
        "id": 32,
        "category": "Data Structures",
        "difficulty": "Easy",
        "question": "What is the average time complexity of accessing an element in an array by its index?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
        "correct_index": 0,
        "explanation": "Arrays provide contiguous memory allocation, allowing instantaneous direct indexing via base_address + (index * size_of_element) in O(1) time."
    },
    {
        "id": 33,
        "category": "Data Structures",
        "difficulty": "Easy",
        "question": "Which data structure is typically used to implement Breadth-First Search (BFS) in a graph?",
        "options": ["Stack", "Queue", "Heap", "Binary Search Tree"],
        "correct_index": 1,
        "explanation": "BFS explores vertices level by level in FIFO order, making a Queue the standard data structure for keeping track of discovered vertices."
    },
    {
        "id": 34,
        "category": "Data Structures",
        "difficulty": "Easy",
        "question": "In a singly linked list, what does the 'next' pointer of the tail node typically point to?",
        "options": ["Head node", "Previous node", "NULL / None", "Itself"],
        "correct_index": 2,
        "explanation": "The tail node in a non-circular singly linked list contains a pointer pointing to NULL (or None in Python) to signify the end of the sequence."
    },
    {
        "id": 35,
        "category": "Data Structures",
        "difficulty": "Easy",
        "question": "What is the minimum number of children a node can have in a standard Binary Tree?",
        "options": ["0", "1", "2", "3"],
        "correct_index": 0,
        "explanation": "A leaf node in a binary tree has 0 children. Every node in a binary tree has between 0 and 2 children."
    },
    {
        "id": 36,
        "category": "Data Structures",
        "difficulty": "Medium",
        "question": "What is the WORST-CASE time complexity of searching in an unbalanced Binary Search Tree (BST)?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "correct_index": 2,
        "explanation": "When elements are inserted in sorted order, an unbalanced BST degenerates into a linear linked list (skewed tree), degrading search to O(n)."
    },
    {
        "id": 37,
        "category": "Data Structures",
        "difficulty": "Medium",
        "question": "In an AVL tree, what is the maximum allowed difference between the heights of the left and right subtrees of any node?",
        "options": ["0", "1", "2", "log n"],
        "correct_index": 1,
        "explanation": "The balance factor of an AVL tree node must be in {-1, 0, 1}. If the height difference exceeds 1, self-balancing rotations are triggered."
    },
    {
        "id": 38,
        "category": "Data Structures",
        "difficulty": "Medium",
        "question": "What is the worst-case time complexity of QuickSort?",
        "options": ["O(n)", "O(n log n)", "O(n^2)", "O(2^n)"],
        "correct_index": 2,
        "explanation": "QuickSort degrades to O(n^2) when the chosen pivot is consistently the smallest or largest element (such as an already sorted array with naive pivot selection)."
    },
    {
        "id": 39,
        "category": "Data Structures",
        "difficulty": "Medium",
        "question": "Which collision resolution technique in Hash Tables stores colliding elements in a linked list at the same index?",
        "options": ["Linear Probing", "Quadratic Probing", "Separate Chaining", "Double Hashing"],
        "correct_index": 2,
        "explanation": "Separate Chaining maintains an independent linked list (or dynamic array) at each bucket index to store multiple colliding keys."
    },
    {
        "id": 40,
        "category": "Data Structures",
        "difficulty": "Medium",
        "question": "How many pointers does a node in a Doubly Linked List maintain?",
        "options": ["1", "2", "3", "0"],
        "correct_index": 1,
        "explanation": "Each node in a doubly linked list contains two pointers: 'prev' pointing to the preceding node and 'next' pointing to the succeeding node."
    },
    {
        "id": 41,
        "category": "Data Structures",
        "difficulty": "Hard",
        "question": "In a Red-Black Tree, which of the following is an invariant property?",
        "options": [
            "Every red node must have two black children (no two consecutive red nodes)",
            "The root node must always be red",
            "Every leaf (NIL) must be red",
            "Left subtree height must equal right subtree height exactly"
        ],
        "correct_index": 0,
        "explanation": "Red-Black tree properties state that the root is black, all NIL leaves are black, no two red nodes can be adjacent, and every simple path to NIL leaves has the same black-height."
    },
    {
        "id": 42,
        "category": "Data Structures",
        "difficulty": "Hard",
        "question": "What is the amortized time complexity of the 'find' and 'union' operations in a Disjoint Set Union (DSU) with Path Compression and Union by Rank?",
        "options": ["O(log n)", "O(n)", "O(α(n)) [Inverse Ackermann]", "O(1) strictly"],
        "correct_index": 2,
        "explanation": "With both path compression and union by rank/size, the amortized cost per operation is O(α(n)), where α is the inverse Ackermann function (effectively ≤ 4 for all practical universe sizes)."
    },
    {
        "id": 43,
        "category": "Data Structures",
        "difficulty": "Hard",
        "question": "What is the primary operational advantage of a B-Tree or B+ Tree over an AVL Tree for database disk storage?",
        "options": [
            "B-Trees use less RAM than basic arrays",
            "High branching factor reduces tree height, minimizing slow secondary storage disk I/O operations",
            "B-Trees eliminate the need for index sorting",
            "B-Trees execute exclusively in GPU memory"
        ],
        "correct_index": 1,
        "explanation": "Disks read data in page blocks. B-Trees have hundreds of children per node, making the tree very shallow (height 3-4 for millions of records), minimizing slow disk head seeks."
    },
    {
        "id": 44,
        "category": "Data Structures",
        "difficulty": "Hard",
        "question": "What is the space complexity of an adjacency matrix representation of a graph with V vertices?",
        "options": ["O(V)", "O(V + E)", "O(V^2)", "O(E^2)"],
        "correct_index": 2,
        "explanation": "An adjacency matrix is a 2D array of dimensions V x V, which always consumes O(V^2) memory regardless of how sparse or dense the edges E are."
    },
    {
        "id": 45,
        "category": "Data Structures",
        "difficulty": "Hard",
        "question": "What is a Trie (Prefix Tree) best suited for?",
        "options": [
            "Finding shortest paths in weighted road networks",
            "Fast prefix matching, dictionary lookup, and autocomplete for strings",
            "Dynamic memory garbage collection",
            "Sorting floating point numbers in O(1) time"
        ],
        "correct_index": 1,
        "explanation": "A Trie stores strings character by character down edges. Lookups, inserts, and prefix queries depend on string length L rather than dictionary size, achieving O(L) time."
    },

    # =========================================================================
    # 4. ARTIFICIAL INTELLIGENCE & MACHINE LEARNING (15 Questions: 5 Easy, 5 Med, 5 Hard)
    # =========================================================================
    {
        "id": 46,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Easy",
        "question": "Who is widely regarded as the 'Father of Artificial Intelligence'?",
        "options": ["Alan Turing", "John McCarthy", "Geoffrey Hinton", "Marvin Minsky"],
        "correct_index": 1,
        "explanation": "John McCarthy coined the term 'Artificial Intelligence' in 1955 and organized the famous 1956 Dartmouth Conference."
    },
    {
        "id": 47,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Easy",
        "question": "Which of the following is an example of SUPERVISED learning?",
        "options": ["K-Means Clustering", "Linear Regression", "Principal Component Analysis (PCA)", "Apriori Algorithm"],
        "correct_index": 1,
        "explanation": "Supervised learning trains on labeled datasets (inputs and target outputs). Linear Regression maps features to target continuous labels."
    },
    {
        "id": 48,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Easy",
        "question": "What does 'Overfitting' mean in machine learning?",
        "options": [
            "The model performs exceptionally well on both training and test data",
            "The model memorizes training noise and fails to generalize to unseen test data",
            "The model is too simple to capture the underlying pattern",
            "The training process runs out of RAM"
        ],
        "correct_index": 1,
        "explanation": "Overfitting happens when a model fits the training set too closely (low bias, high variance), resulting in poor generalization on new data."
    },
    {
        "id": 49,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Easy",
        "question": "Which activation function outputs values strictly in the range (0, 1)?",
        "options": ["ReLU", "Sigmoid", "Tanh", "Leaky ReLU"],
        "correct_index": 1,
        "explanation": "The Sigmoid function σ(z) = 1 / (1 + e^(-z)) maps any real number to a value between 0 and 1, often interpreted as a probability."
    },
    {
        "id": 50,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Easy",
        "question": "What does 'NLP' stand for in Artificial Intelligence?",
        "options": [
            "Natural Language Processing",
            "Network Level Protocol",
            "Neural Learning Program",
            "Non-Linear Programming"
        ],
        "correct_index": 0,
        "explanation": "NLP stands for Natural Language Processing, a subfield of AI concerned with giving computers the ability to understand text and spoken words."
    },
    {
        "id": 51,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Medium",
        "question": "What is the primary purpose of the Cost / Loss function in machine learning?",
        "options": [
            "To measure the financial cost of cloud GPUs",
            "To quantify the error between model predictions and actual ground truth labels",
            "To count the number of hidden layers",
            "To format the output as a PDF report"
        ],
        "correct_index": 1,
        "explanation": "A loss function calculates the difference (penalty) between predicted outputs and real targets, providing a scalar gradient to guide optimization."
    },
    {
        "id": 52,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Medium",
        "question": "In a Confusion Matrix, what does 'Recall' (Sensitivity) measure?",
        "options": [
            "TP / (TP + FP)",
            "TP / (TP + FN)",
            "(TP + TN) / (TP + TN + FP + FN)",
            "TN / (TN + FP)"
        ],
        "correct_index": 1,
        "explanation": "Recall is True Positives divided by total actual positive instances (TP + FN). It measures the model's ability to identify all relevant instances."
    },
    {
        "id": 53,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Medium",
        "question": "Why is the ReLU (Rectified Linear Unit) activation function favored over Sigmoid in deep neural networks?",
        "options": [
            "It eliminates vanishing gradient problems for positive inputs and is computationally cheap: max(0, x)",
            "It keeps values bounded strictly between -1 and +1",
            "It performs matrix inversion automatically",
            "It guarantees 100% classification accuracy"
        ],
        "correct_index": 0,
        "explanation": "Sigmoid saturates at both tails with near-zero gradients. ReLU has derivative 1 for all x > 0, mitigating vanishing gradients and computing fast."
    },
    {
        "id": 54,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Medium",
        "question": "What is the key mechanism behind Ensemble Learning methods like Random Forest?",
        "options": [
            "Using a single gigantic decision tree with million nodes",
            "Combining predictions of multiple diverse decision trees (bagging) to reduce variance",
            "Replacing gradient descent with genetic mutations",
            "Clustering images without human supervision"
        ],
        "correct_index": 1,
        "explanation": "Random Forest uses bootstrap aggregating (bagging) and random feature selection over an ensemble of trees to lower variance and resist overfitting."
    },
    {
        "id": 55,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Medium",
        "question": "Which search algorithm in AI uses an evaluation function f(n) = g(n) + h(n)?",
        "options": ["Minimax Algorithm", "A* (A-Star) Search", "Breadth-First Search", "Depth-First Search"],
        "correct_index": 1,
        "explanation": "A* search evaluates nodes with f(n) = g(n) + h(n), where g(n) is actual cost from start to n, and h(n) is an admissible heuristic estimate to the goal."
    },
    {
        "id": 56,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Hard",
        "question": "What breakthrough architecture introduced the 'Self-Attention' mechanism in the paper 'Attention Is All You Need' (Vaswani et al., 2017)?",
        "options": ["Convolutional Neural Network (CNN)", "Transformer", "Recurrent Neural Network (RNN)", "Hopfield Network"],
        "correct_index": 1,
        "explanation": "The Transformer architecture replaced recurrence entirely with Multi-Head Self-Attention, powering modern Large Language Models (LLMs)."
    },
    {
        "id": 57,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Hard",
        "question": "What is the difference between L1 (Lasso) and L2 (Ridge) Regularization?",
        "options": [
            "L1 adds squared weights; L2 adds absolute weights",
            "L1 adds absolute penalty |w|, driving irrelevant feature weights to exact zero (sparsity); L2 adds w^2, shrinking weights smoothly",
            "L1 is for classification only; L2 is for regression only",
            "There is no mathematical difference"
        ],
        "correct_index": 1,
        "explanation": "L1 norm produces diamond-shaped constraint boundaries that intersect axes, producing sparse solutions (feature selection). L2 penalizes large weights proportionally."
    },
    {
        "id": 58,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Hard",
        "question": "In Reinforcement Learning, what equation expresses the optimal action-value function Q*(s, a) recursively?",
        "options": ["Navier-Stokes Equation", "Bellman Optimality Equation", "Schrödinger Equation", "Shannon Entropy Formula"],
        "correct_index": 1,
        "explanation": "The Bellman Optimality Equation expresses that Q*(s, a) = R(s, a) + γ * max_a' [Q*(s', a')], underpinning Q-Learning and dynamic programming."
    },
    {
        "id": 59,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Hard",
        "question": "What issue in Deep Recurrent Neural Networks (RNNs) do Long Short-Term Memory (LSTM) networks specifically resolve?",
        "options": [
            "GPU memory fragmentation",
            "Vanishing and exploding gradients across long temporal sequences using gated cell states",
            "Over-dependence on convolutional kernels",
            "Inability to handle numerical inputs"
        ],
        "correct_index": 1,
        "explanation": "LSTMs use input, forget, and output gates along with an additive constant-error carousel (cell state) to allow gradients to flow across hundreds of timesteps."
    },
    {
        "id": 60,
        "category": "Artificial Intelligence and Machine Learning",
        "difficulty": "Hard",
        "question": "In a Generative Adversarial Network (GAN), what are the two competing neural networks?",
        "options": [
            "Encoder and Decoder",
            "Generator and Discriminator",
            "Actor and Critic",
            "Feedforward and Recurrent"
        ],
        "correct_index": 1,
        "explanation": "The Generator creates synthetic samples from random noise, while the Discriminator tries to distinguish real data from generated fakes in a minimax game."
    },

    # =========================================================================
    # 5. GENERAL KNOWLEDGE (15 Questions: 5 Easy, 5 Medium, 5 Hard)
    # =========================================================================
    {
        "id": 61,
        "category": "General Knowledge",
        "difficulty": "Easy",
        "question": "Which planet in our solar system is known as the 'Red Planet'?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct_index": 1,
        "explanation": "Mars appears reddish due to the prevalence of iron oxide (rust) across its planetary surface."
    },
    {
        "id": 62,
        "category": "General Knowledge",
        "difficulty": "Easy",
        "question": "What is the capital city of France?",
        "options": ["Rome", "Berlin", "Paris", "Madrid"],
        "correct_index": 2,
        "explanation": "Paris is the capital and most populous city of France, located on the Seine River."
    },
    {
        "id": 63,
        "category": "General Knowledge",
        "difficulty": "Easy",
        "question": "Which element has the chemical symbol 'O' and atomic number 8?",
        "options": ["Osmium", "Oxygen", "Gold", "Iron"],
        "correct_index": 1,
        "explanation": "Oxygen has atomic number 8 and chemical symbol 'O'. It constitutes about 21% of Earth's atmosphere."
    },
    {
        "id": 64,
        "category": "General Knowledge",
        "difficulty": "Easy",
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct_index": 3,
        "explanation": "The Pacific Ocean is the largest and deepest ocean on Earth, covering more than 30% of the planet's surface."
    },
    {
        "id": 65,
        "category": "General Knowledge",
        "difficulty": "Easy",
        "question": "Who painted the famous masterpiece 'Mona Lisa'?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "correct_index": 2,
        "explanation": "Leonardo da Vinci, the Italian Renaissance polymath, painted the Mona Lisa in the early 16th century."
    },
    {
        "id": 66,
        "category": "General Knowledge",
        "difficulty": "Medium",
        "question": "Which treaty signed in 1919 officially brought an end to World War I?",
        "options": ["Treaty of Paris", "Treaty of Versailles", "Treaty of Utrecht", "Geneva Convention"],
        "correct_index": 1,
        "explanation": "The Treaty of Versailles, signed on June 28, 1919 in the Hall of Mirrors, formally ended the state of war between Germany and the Allied Powers."
    },
    {
        "id": 67,
        "category": "General Knowledge",
        "difficulty": "Medium",
        "question": "What is the SI unit of electric resistance?",
        "options": ["Ampere", "Volt", "Ohm", "Watt"],
        "correct_index": 2,
        "explanation": "The Ohm (symbol: Ω), named after German physicist Georg Simon Ohm, is the SI derived unit of electrical resistance."
    },
    {
        "id": 68,
        "category": "General Knowledge",
        "difficulty": "Medium",
        "question": "Which Indian city is famously known as the 'Silicon Valley of India'?",
        "options": ["Hyderabad", "Bengaluru (Bangalore)", "Pune", "Chennai"],
        "correct_index": 1,
        "explanation": "Bengaluru is nicknamed the Silicon Valley of India because it is the nation's leading information technology exporter and tech hub."
    },
    {
        "id": 69,
        "category": "General Knowledge",
        "difficulty": "Medium",
        "question": "Who was the first person to walk on the surface of the Moon in July 1969?",
        "options": ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "Michael Collins"],
        "correct_index": 2,
        "explanation": "American astronaut Neil Armstrong became the first human to step onto the lunar surface during the Apollo 11 mission on July 20, 1969."
    },
    {
        "id": 70,
        "category": "General Knowledge",
        "difficulty": "Medium",
        "question": "Which organ in the human body is primarily responsible for filtering waste from blood to form urine?",
        "options": ["Liver", "Kidneys", "Pancreas", "Lungs"],
        "correct_index": 1,
        "explanation": "The kidneys filter approximately 120-150 quarts of blood daily to eliminate waste products, regulate fluid balance, and produce urine."
    },
    {
        "id": 71,
        "category": "General Knowledge",
        "difficulty": "Hard",
        "question": "What is the rarest blood type in the human ABO and Rh blood group system?",
        "options": ["O Positive", "A Negative", "AB Negative", "B Negative"],
        "correct_index": 2,
        "explanation": "AB Negative is the rarest ABO-Rh blood type, occurring in less than 1% of the global population."
    },
    {
        "id": 72,
        "category": "General Knowledge",
        "difficulty": "Hard",
        "question": "Which fundamental particle of the Standard Model was experimentally observed at CERN's LHC in 2012, confirming the origin of particle mass?",
        "options": ["Tau Neutrino", "Top Quark", "Higgs Boson", "Graviton"],
        "correct_index": 2,
        "explanation": "The Higgs Boson, predicted by Peter Higgs and colleagues in 1964, was confirmed at CERN in 2012, validating the mechanism that gives elementary particles mass."
    },
    {
        "id": 73,
        "category": "General Knowledge",
        "difficulty": "Hard",
        "question": "Which ancient wonder of the world was located in the city of Alexandria, Egypt?",
        "options": [
            "Colossus of Rhodes",
            "Pharos (Lighthouse) of Alexandria",
            "Hanging Gardens of Babylon",
            "Temple of Artemis"
        ],
        "correct_index": 1,
        "explanation": "The Lighthouse of Alexandria (Pharos), built by the Ptolemaic Kingdom around 280 BC, stood over 100 meters tall on the island of Pharos."
    },
    {
        "id": 74,
        "category": "General Knowledge",
        "difficulty": "Hard",
        "question": "In computer history, who wrote the world's first algorithm intended to be processed by Charles Babbage's Analytical Engine?",
        "options": ["Ada Lovelace", "Grace Hopper", "Margaret Hamilton", "Katherine Johnson"],
        "correct_index": 0,
        "explanation": "Ada Lovelace published the first algorithm to calculate Bernoulli numbers using the Analytical Engine in 1843, making her the world's first computer programmer."
    },
    {
        "id": 75,
        "category": "General Knowledge",
        "difficulty": "Hard",
        "question": "What is the deepest known oceanic trench on Earth?",
        "options": ["Java Trench", "Puerto Rico Trench", "Mariana Trench (Challenger Deep)", "Tonga Trench"],
        "correct_index": 2,
        "explanation": "The Challenger Deep in the Mariana Trench reaches a depth of approximately 10,994 meters (nearly 36,000 feet) below sea level."
    }
]


def get_categories():
    """Return the list of all available categories."""
    return list(CATEGORIES)


def get_difficulties():
    """Return the list of supported difficulty levels."""
    return list(DIFFICULTY_LEVELS)


def get_questions_by_filter(category=None, difficulty=None, limit=None):
    """
    Filter questions by category and/or difficulty.
    If category is 'All', it includes questions from all categories.
    If difficulty is 'All', it includes questions of all difficulties.
    """
    filtered = QUESTIONS_DATA
    if category and category != "All":
        filtered = [q for q in filtered if q["category"] == category]
    if difficulty and difficulty != "All":
        filtered = [q for q in filtered if q["difficulty"] == difficulty]
    
    if limit is not None and limit > 0:
        return filtered[:limit]
    return filtered


def get_questions_by_ids(id_list):
    """
    Return a list of question dictionaries corresponding to the given IDs,
    preserving the order specified in id_list.
    """
    if not id_list:
        return []
    lookup = {q["id"]: q for q in QUESTIONS_DATA}
    results = []
    for raw_id in id_list:
        try:
            qid = int(raw_id)
            if qid in lookup:
                results.append(lookup[qid])
        except (ValueError, TypeError):
            continue
    return results
