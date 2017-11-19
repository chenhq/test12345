def cumulate_return(returns):
    return (returns.fillna(0) + 1).cumprod()
