# import pytest
# import scipy.stats
# import pandas as pd
# from fcapy.tools import generate_rank_df, calculate_rank_correlation

# df1 = pd.DataFrame([[1, 1],
#                     [1, 1],
#                     [2, 2],
#                     [3, 3]])
# df2 = pd.DataFrame([[1, 1],
#                     [1, 1],
#                     [2, 4],
#                     [3, 3]])
# df3 = pd.DataFrame([[1, 2],
#                     [1, 1],
#                     [2, 1]])
# df4 = pd.DataFrame([[1, 3],
#                     [2, 2],
#                     [3, 1]])


# def test_generate_rank_df():
#     expected_df = pd.DataFrame([[0, 0], [1, 1], [2, 2], [3, 3]])

#     assert expected_df.equals(generate_rank_df(df1))

#     expected_df = pd.DataFrame([[0, 0], [1, 1], [2, 3], [3, 2]])

#     assert expected_df.equals(generate_rank_df(df2))

#     expected_df = pd.DataFrame([[0, 1], [1, 2], [2, 0]])

#     assert expected_df.equals(generate_rank_df(df3))

#     expected_df = pd.DataFrame([[0, 2], [1, 1], [2, 0]])

#     assert expected_df.equals(generate_rank_df(df4))


# def test_generate_rank_df_descending():
#     expected_df = pd.DataFrame([[3, 3], [2, 2], [0, 0], [1, 1], ])

#     assert expected_df.equals(generate_rank_df(df1, ascending=False))

#     expected_df = pd.DataFrame([[3, 2], [2, 3], [0, 0], [1, 1]])

#     assert expected_df.equals(generate_rank_df(df2, ascending=False))

#     expected_df = pd.DataFrame([[2, 0], [0, 1], [1, 2]])

#     assert expected_df.equals(generate_rank_df(df3, ascending=False))

#     expected_df = pd.DataFrame([[2, 0], [1, 1], [0, 2]])

#     assert expected_df.equals(generate_rank_df(df4, ascending=False))


# @pytest.mark.parametrize("df", [df1, df2, df3, df4])
# def test_calculate_rank_correlation(df):
#     df_order = generate_rank_df(df)
#     df_corr = calculate_rank_correlation(df_order, scipy.stats.kendalltau)

#     assert scipy.stats.kendalltau(df_order[0], df_order[0])[0] == df_corr[0][0]
#     assert scipy.stats.kendalltau(df_order[0], df_order[1])[0] == df_corr[0][1]
#     assert scipy.stats.kendalltau(df_order[1], df_order[0])[0] == df_corr[1][0]
#     assert scipy.stats.kendalltau(df_order[1], df_order[1])[0] == df_corr[1][1]
