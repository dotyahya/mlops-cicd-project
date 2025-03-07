def load_sample_data():
    """
    Load sample sentiment analysis dataset
    Returns:
        tuple: (X, y) where X is list of texts and y is list of labels (0 for negative, 1 for positive)
    """
    texts = [
        "This is amazing!",
        "I love this product",
        "Great service",
        "Excellent work",
        "This is terrible",
        "Poor quality",
        "Bad experience",
        "Not recommended"
    ]
    
    labels = [1, 1, 1, 1, 0, 0, 0, 0]  # 1 for positive, 0 for negative
    
    return texts, labels 