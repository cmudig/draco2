from draco.asp_utils import Block
from draco.programs import define, helpers, soft
from draco.run import run_clingo


def list_preferences(program: str):
    try:
        model = next(run_clingo(helpers.program + define.program + program, 1))

        return sorted(
            [
                tuple(map(lambda x: x.name, symbol.arguments))
                for symbol in model.answer_set
                if symbol.name == "preference"
            ]
        )

    except StopIteration:
        return None


def test_list_preferences():
    assert list_preferences(":- a. :- not a.") is None


def test_aggregate():
    b = soft.blocks["aggregate"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((encoding,aggregate),e1,mean).
    """
    ) == [("aggregate", "e1")]

    assert list_preferences(
        b.program
        + """
    attribute((encoding,aggregate),e1,mean).
    attribute((encoding,aggregate),e2,mean).
    """
    ) == [("aggregate", "e1"), ("aggregate", "e2")]


def test_bin():
    b = soft.blocks["bin"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((encoding,binning),e1,10).
    """
    ) == [("bin", "e1")]

    assert list_preferences(
        b.program
        + """
    attribute((encoding,binning),e1,10).
    attribute((encoding,binning),e2,20).
    """
    ) == [("bin", "e1"), ("bin", "e2")]


def test_bin_high():
    b = soft.blocks["bin_high"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
     attribute((encoding,binning),e1,8).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((encoding,binning),e1,13).
    """
    ) == [("bin_high", "e1")]

    assert list_preferences(
        b.program
        + """
    attribute((encoding,binning),e1,14).
    attribute((encoding,binning),e2,20).
    """
    ) == [("bin_high", "e1"), ("bin_high", "e2")]


def test_bin_low():
    b = soft.blocks["bin_low"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,8).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((encoding,binning),e1,3).
    """
    ) == [("bin_low", "e1")]

    assert list_preferences(
        b.program
        + """
    attribute((encoding,binning),e1,7).
    attribute((encoding,binning),e2,3).
    """
    ) == [("bin_low", "e1"), ("bin_low", "e2")]


def test_encoding():
    b = soft.blocks["encoding"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    """
    ) == [("encoding", "e1")]

    assert list_preferences(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    entity(encoding,m1,e2).
    """
    ) == [("encoding", "e1"), ("encoding", "e2")]


def test_encoding_field():
    b = soft.blocks["encoding_field"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,aggregate),e1,mean).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((encoding,field),e1,temperature).
    """
    ) == [("encoding_field", "e1")]

    assert list_preferences(
        b.program
        + """
    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,date).
    """
    ) == [("encoding_field", "e1"), ("encoding_field", "e2")]


def test_same_field():
    b = soft.blocks["same_field"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).
    entity(field,root,date).

    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,date).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(field,root,temperature).

    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,temperature).
    """
    ) == [("same_field", "temperature")]

    assert list_preferences(
        b.program
        + """
    entity(field,root,temperature).
    entity(field,root,date).

    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).
    entity(encoding,m,e3).
    entity(encoding,m,e4).

    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,temperature).
    helper((encoding,field),e3,date).
    helper((encoding,field),e4,date).
    """
    ) == [("same_field", "date"), ("same_field", "temperature")]

    # use field temperature twice with mark m1, and field date with 2 different marks
    assert list_preferences(
        b.program
        + """
    entity(field,root,temperature).
    entity(field,root,date).

    entity(mark,v,m1).
    entity(mark,v,m2).

    entity(encoding,m1,e1).
    entity(encoding,m1,e2).
    entity(encoding,m2,e3).
    entity(encoding,m1,e4).

    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,temperature).
    helper((encoding,field),e3,date).
    helper((encoding,field),e4,date).
    """
    ) == [("same_field", "temperature")]


def test_same_field_grt3():
    b = soft.blocks["same_field_grt3"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).
    entity(field,root,date).

    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,date).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).

    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,temperature).
    """
        )
        == []
    )

    # use field temperature 3 times, but with 2 different marks.
    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).

    entity(mark,v,m1).
    entity(mark,v,m2).

    entity(encoding,m1,e1).
    entity(encoding,m1,e2).
    entity(encoding,m2,e3).


    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,temperature).
    helper((encoding,field),e3,temperature).
    """
        )
        == []
    )

    # use field temperature 3 times with the same mark
    assert list_preferences(
        b.program
        + """
    entity(field,root,temperature).

    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).
    entity(encoding,m,e3).

    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,temperature).
    helper((encoding,field),e3,temperature).
    """
    ) == [("same_field_grt3", "temperature")]

    # use field temperature 4 times with the same mark
    assert list_preferences(
        b.program
        + """
    entity(field,root,temperature).

    entity(mark,v,m).

    entity(encoding,m,e1).
    entity(encoding,m,e2).
    entity(encoding,m,e3).
    entity(encoding,m,e4).

    helper((encoding,field),e1,temperature).
    helper((encoding,field),e2,temperature).
    helper((encoding,field),e3,temperature).
    helper((encoding,field),e4,temperature).
    """
    ) == [("same_field_grt3", "temperature")]


def test_count_grt1():
    b = soft.blocks["count_grt1"]
    assert isinstance(b, Block)

    # only 1 count
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,aggregate),e1,count).
    """
        )
        == []
    )

    # 2 aggregate, but not only 1 count
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    attribute((encoding,aggregate),e1,sum).
    attribute((encoding,aggregate),e2,count).
    """
        )
        == []
    )

    # 2 counts
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    attribute((encoding,aggregate),e1,count).
    attribute((encoding,aggregate),e2,count).
    """
    ) == [("count_grt1", "m")]

    # 3 counts
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).
    entity(encoding,m,e3).

    attribute((encoding,aggregate),e1,count).
    attribute((encoding,aggregate),e2,count).
    attribute((encoding,aggregate),e3,count).
    """
    ) == [("count_grt1", "m")]


def test_number_categorical():
    b = soft.blocks["number_categorical"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # root scale, categorical for number
    assert list_preferences(
        b.program
        + """
    attribute((field,type),temperature,number).

    entity(view,root,v).
    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,categorical).
    """
    ) == [("number_categorical", "e1")]

    # two scales, categorical for number
    assert list_preferences(
        b.program
        + """
    attribute((field,type),temperature,number).

    entity(mark,v1,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,v1,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,categorical).
    """
    ) == [("number_categorical", "e1")]

    # number field used for two times (in same mark)
    assert list_preferences(
        b.program
        + """
    attribute((field,type),temperature,number).

    entity(mark,v1,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    helper((encoding,field),e2,temperature).
    attribute((encoding,channel),e2,color).

    entity(scale,v1,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v1,s2).
    attribute((scale,channel),s2,color).
    attribute((scale,type),s2,categorical).
    """
    ) == [("number_categorical", "e2")]


def test_bin_low_unique():
    b = soft.blocks["bin_low_unique"]
    assert isinstance(b, Block)

    # number
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).
    attribute((field,unique),temperature,50).
    helper((encoding,field),e1,temperature).
    attribute((encoding,binning),e1,20).
    """
        )
        == []
    )

    # datetime
    assert list_preferences(
        b.program
        + """
    attribute((field,type),date,datetime).
    attribute((field,unique),date,10).
    helper((encoding,field),e1,date).
    attribute((encoding,binning),e1,5).
    """
    ) == [("bin_low_unique", "e1")]


def test_bin_not_linear():
    b = soft.blocks["bin_not_linear"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,15).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,15).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # log scale
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,15).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,log).
    """
    ) == [("bin_not_linear", "e1")]


def test_only_discrete():
    b = soft.blocks["only_discrete"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # 1 encoding
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
    ) == [("only_discrete", "m1")]

    # 2 encodings
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("only_discrete", "m1")]

    # shared scale
    assert list_preferences(
        b.program
        + """
    entity(view,root,v1).
    entity(mark,v1,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).

    entity(view,root,v2).
    entity(mark,v2,m2).
    entity(encoding,m2,e3).
    attribute((encoding,channel),e3,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).

    entity(scale,v2,s2).
    attribute((scale,channel),s2,color).
    attribute((scale,type),s2,categorical).
    """
    ) == [("only_discrete", "m1"), ("only_discrete", "m2")]


def test_multi_non_pos():
    b = soft.blocks["multi_non_pos"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,size).
    """
    ) == [("multi_non_pos", "m1")]


def test_non_pos_used_before_pos():
    b = soft.blocks["non_pos_used_before_pos"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    """
        )
        == []
    )

    # both x and y are not used yet
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).
    """
    ) == [("non_pos_used_before_pos", "m1")]

    # x is not used yet
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,color).
    """
    ) == [("non_pos_used_before_pos", "m1")]


def test_aggregate_group_by_raw():
    b = soft.blocks["aggregate_group_by_raw"]
    assert isinstance(b, Block)

    # discrete: bin
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,count).

    entity(encoding,m1,e2).
    attribute((encoding,binning),e2,10).
    """
        )
        == []
    )

    # discrete scale
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,count).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # aggregate, not raw continuous
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,count).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,x).
    attribute((encoding,aggregate),e2,max).
    """
        )
        == []
    )

    # raw continuous
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,count).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("aggregate_group_by_raw", "e2")]


def test_aggregate_no_discrete():
    b = soft.blocks["aggregate_no_discrete"]
    assert isinstance(b, Block)

    # discrete: bin
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,count).

    entity(encoding,m1,e2).
    attribute((encoding,binning),e2,10).
    """
        )
        == []
    )

    # discrete scale
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,count).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # aggregate continuous
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,count).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,x).
    attribute((encoding,aggregate),e2,max).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("aggregate_no_discrete", "m1")]

    # raw continuous
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,count).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("aggregate_no_discrete", "m1")]


def test_x_y_raw():
    b = soft.blocks["x_y_raw"]
    assert isinstance(b, Block)

    # x discrete, color raw continuous
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).

    entity(scale,v,s2).
    attribute((scale,channel),s2,color).
    attribute((scale,type),s2,linear).
    """
        )
        == []
    )

    # x, y discrete, but size is aggregate
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(encoding,m1,e3).
    attribute((encoding,channel),e3,size).
    attribute((encoding,aggregate),e3,mean).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,ordinal).

    entity(scale,v,s3).
    attribute((scale,channel),s3,size).
    attribute((scale,type),s3,linear).
    """
        )
        == []
    )

    # x discrete, y continuous, color raw continuous
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(encoding,m1,e3).
    attribute((encoding,channel),e3,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,linear).

    entity(scale,v,s3).
    attribute((scale,channel),s3,color).
    attribute((scale,type),s3,linear).
    """
        )
        == []
    )

    # x, y discrete, color raw continuous
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(encoding,m1,e3).
    attribute((encoding,channel),e3,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,ordinal).

    entity(scale,v,s3).
    attribute((scale,channel),s3,color).
    attribute((scale,type),s3,linear).
    """
    ) == [("x_y_raw", "m1")]


def test_continuous_not_zero():
    b = soft.blocks["continuous_not_zero"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    attribute((scale,zero),s1,true).
    """
        )
        == []
    )

    # bin no need to zero
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("continuous_not_zero", "e1")]


def test_size_not_zero():
    b = soft.blocks["size_not_zero"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    attribute((scale,zero),s1,true).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
    ) == [("size_not_zero", "e1")]

    # even bin needs to zero
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).
    attribute((encoding,binning),e1,10).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("size_not_zero", "e1")]


def test_continuous_pos_not_zero():
    b = soft.blocks["continuous_pos_not_zero"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    attribute((scale,zero),s1,true).
    """
        )
        == []
    )

    # bin no need to zero
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("continuous_pos_not_zero", "e1")]

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,linear).
    """
    ) == [("continuous_pos_not_zero", "e1"), ("continuous_pos_not_zero", "e2")]


def test_skew_zero():
    b = soft.blocks["skew_zero"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,min),temperature,5).
    attribute((field,max),temperature,20).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e,temperature).
    attribute((encoding,channel),e1,y).

    entity(scale,v,s).
    attribute((scale,channel),s,y).
    attribute((scale,zero),s,true).
    """
        )
        == []
    )

    # both max and min are positive
    assert list_preferences(
        b.program
        + """
    attribute((field,min),temperature,800).
    attribute((field,max),temperature,1000).

    entity(mark,v,m).
    entity(encoding,m,e).
    helper((encoding,field),e,temperature).
    attribute((encoding,channel),e,y).

    entity(scale,v,s).
    attribute((scale,channel),s,y).
    attribute((scale,zero),s,true).
    """
    ) == [("skew_zero", "e")]

    # both max and min are negative
    assert list_preferences(
        b.program
        + """
    attribute((field,min),temperature,-500).
    attribute((field,max),temperature,-700).

    entity(mark,v,m).
    entity(encoding,m,e).
    helper((encoding,field),e,temperature).
    attribute((encoding,channel),e,y).

    entity(scale,v,s).
    attribute((scale,channel),s,y).
    attribute((scale,zero),s,true).
    """
    ) == [("skew_zero", "e")]


def test_cross_zero():
    b = soft.blocks["cross_zero"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,min),temperature,0).
    attribute((field,max),temperature,200).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e,temperature).
    attribute((encoding,channel),e1,y).

    entity(scale,v,s).
    attribute((scale,channel),s,y).
    attribute((scale,zero),s,true).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((field,min),temperature,-200).
    attribute((field,max),temperature,1000).

    entity(mark,v,m).
    entity(encoding,m,e).
    helper((encoding,field),e,temperature).
    attribute((encoding,channel),e,y).

    entity(scale,v,s).
    attribute((scale,channel),s,y).
    attribute((scale,zero),s,true).
    """
    ) == [("cross_zero", "e")]


def test_only_y():
    b = soft.blocks["only_y"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    """
        )
        == []
    )

    # 1 mark with channel y and size
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,size).
    """
    ) == [("only_y", "m1")]

    # 2 marks
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(mark,v,m2).
    entity(encoding,m2,e2).
    attribute((encoding,channel),e2,x).
    """
    ) == [("only_y", "m1")]


def test_binned_orientation_not_x():
    b = soft.blocks["binned_orientation_not_x"]
    assert isinstance(b, Block)

    # number
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).
    helper((encoding,field),e1,temperature).
    attribute((encoding,binning),e1,20).
    attribute((encoding,channel),e1,x).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).
    helper((encoding,field),e1,temperature).
    attribute((encoding,binning),e1,20).
    attribute((encoding,channel),e1,x).

    helper((encoding,field),e2,temperature).
    attribute((encoding,binning),e2,20).
    attribute((encoding,channel),e2,y).
    """
        )
        == []
    )

    # datetime
    assert list_preferences(
        b.program
        + """
    attribute((field,type),date,datetime).
    helper((encoding,field),e1,date).
    attribute((encoding,binning),e1,20).
    attribute((encoding,channel),e1,y).
    """
    ) == [("binned_orientation_not_x", "e1")]


def test_high_cardinality_ordinal():
    b = soft.blocks["high_cardinality_ordinal"]
    assert isinstance(b, Block)

    # low cardinality: binning
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,1461).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,20).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # high cardinality: unique
    assert list_preferences(
        b.program
        + """
    attribute((field,unique),date,1461).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("high_cardinality_ordinal", "e1")]


def test_high_cardinality_categorical_grt10():
    b = soft.blocks["high_cardinality_categorical_grt10"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),weather,5).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,weather).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((field,unique),weather,15).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,weather).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
    ) == [("high_cardinality_categorical_grt10", "e1")]


def test_high_cardinality_shape():
    b = soft.blocks["high_cardinality_shape"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,25).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,shape).
    attribute((encoding,binning),e1,5).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((field,unique),weather,15).
    helper((encoding,field),e1,weather).
    attribute((encoding,channel),e1,shape).
    """
    ) == [("high_cardinality_shape", "e1")]


def test_high_cardinality_size():
    b = soft.blocks["high_cardinality_size"]
    assert isinstance(b, Block)

    # x is not continuous, binning
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,1461).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,binning),e1,20).
    attribute((encoding,channel),e1,x).

    entity(encoding,m,e2).
    attribute((encoding,channel),e1,size).
    """
        )
        == []
    )

    # x is not continuous, ordinal scale
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),weather,150).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,weather).
    attribute((encoding,channel),e1,x).

    entity(encoding,m,e2).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # y is continuous with high cardinality
    assert list_preferences(
        b.program
        + """
    attribute((field,unique),temperature,150).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,y).

    entity(encoding,m,e2).
    attribute((encoding,channel),e2,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,linear).
    """
    ) == [("high_cardinality_size", "e1")]


def test_horizontal_scrolling_x():
    b = soft.blocks["horizontal_scrolling_x"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,1461).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,20).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,1461).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((field,unique),date,1461).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("horizontal_scrolling_x", "e1")]


def test_horizontal_scrolling_col():
    b = soft.blocks["horizontal_scrolling_col"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),fd,1461).
    attribute((field,name),fd,date).

    entity(facet,v,f).
    attribute((facet,field),f,date).
    attribute((facet,channel),f,col).
    attribute((facet,binning),f,5).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((field,unique),fd,1461).
    attribute((field,name),fd,date).

    entity(facet,v,f).
    attribute((facet,field),f,date).
    attribute((facet,channel),f,col).
    """
    ) == [("horizontal_scrolling_col", "f")]


def test_date_scale():
    b = soft.blocks["date_scale"]
    assert isinstance(b, Block)

    # scale on view, linear
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),date,datetime).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root, ordinal
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),date,datetime).

    entity(view,root,v).
    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # scale on view, log
    assert list_preferences(
        b.program
        + """
    attribute((field,type),date,datetime).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,log).
    """
    ) == [("date_scale", "e1")]

    # scale on root, categorical
    assert list_preferences(
        b.program
        + """
    attribute((field,type),date,datetime).

    entity(view,root,v).
    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
    ) == [("date_scale", "e1")]


def test_number_linear():
    b = soft.blocks["number_linear"]
    assert isinstance(b, Block)

    # scale on view, linear
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).
    attribute((field,unique),temperature,111).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root, with binning, ordinal
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).
    attribute((field,unique),temperature,111).

    entity(view,root,v).
    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,20).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # scale on view, ordinal
    assert list_preferences(
        b.program
        + """
    attribute((field,type),temperature,number).
    attribute((field,unique),temperature,111).

    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("number_linear", "e1")]

    # scale on root, log
    assert list_preferences(
        b.program
        + """
    attribute((field,type),temperature,number).
    attribute((field,unique),temperature,111).

    entity(view,root,v).
    entity(mark,v,m).
    entity(encoding,m,e1).
    helper((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,log).
    """
    ) == [("number_linear", "e1")]


def test_value_agg():
    b = soft.blocks["value_agg"]
    assert isinstance(b, Block)

    # value task, no agg
    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,binning),e1,20).
    """
        )
        == []
    )

    # summary task, v has agg
    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,max).
    """
        )
        == []
    )

    # value task, v1 has agg
    assert list_preferences(
        b.program
        + """
    attribute(task,root,value).

    entity(view,root,v1).
    entity(mark,v1,m1).
    entity(encoding,m1,e1).
    attribute((encoding,aggregate),e1,max).

    entity(view,root,v2).
    entity(mark,v2,m2).
    entity(encoding,m2,e2).
    attribute((encoding,binning),e2,20).
    """
    ) == [("value_agg", "v1")]


def test_summary_facet():
    b = soft.blocks["summary_facet"]
    assert isinstance(b, Block)

    # summary task, no facet
    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,binning),e1,20).
    """
        )
        == []
    )

    # value task, v has facet
    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(view,root,v).
    entity(facet,v,f).
    """
        )
        == []
    )

    # summary task, v has facet
    assert list_preferences(
        b.program
        + """
    attribute(task,root,summary).

    entity(view,root,v1).
    entity(facet,v1,f).

    entity(view,root,v2).
    entity(mark,v2,m1).
    entity(encoding,m1,e1).
    attribute((encoding,binning),e1,20).
    """
    ) == [("summary_facet", "v1")]


def test_c_d_col():
    b = soft.blocks["c_d_col"]
    assert isinstance(b, Block)

    # continuous x, discrete y (binning), row
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).

    entity(facet,v,f).
    attribute((facet,channel),f,row).
    """
        )
        == []
    )

    # continuous y, discrete x (binning), column
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(facet,v,f).
    attribute((facet,channel),f,col).
    """
        )
        == []
    )

    # continuous x, discrete y (ordinal), column
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,ordinal).

    entity(facet,v,f).
    attribute((facet,channel),f,col).
    """
    ) == [("c_d_col", "v")]


def test_date_not_x():
    b = soft.blocks["date_not_x"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),date,datetime).

    entity(encoding,m1,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute((field,type),date,datetime).

    entity(encoding,m1,e1).
    helper((encoding,field),e1,date).
    attribute((encoding,channel),e1,y).
    """
    ) == [("date_not_x", "e1")]


def test_x_row():
    b = soft.blocks["x_row"]
    assert isinstance(b, Block)

    # x and row not in the same view
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v1,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(facet,v2,f1).
    attribute((facet,channel),f1,row).
    """
        )
        == []
    )

    # x and col in the same view
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(facet,v,f1).
    attribute((facet,channel),f1,col).
    """
        )
        == []
    )

    # x and row in the same view
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(facet,v,f1).
    attribute((facet,channel),f1,row).
    """
    ) == [("x_row", "v")]


def test_y_row():
    b = soft.blocks["y_row"]
    assert isinstance(b, Block)

    # y and row not in the same view
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v1,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(facet,v2,f1).
    attribute((facet,channel),f1,row).
    """
        )
        == []
    )

    # y and col in the same view
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(facet,v,f1).
    attribute((facet,channel),f1,col).
    """
        )
        == []
    )

    # y and row in the same view
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(facet,v,f1).
    attribute((facet,channel),f1,row).
    """
    ) == [("y_row", "v")]


def test_x_col():
    b = soft.blocks["x_col"]
    assert isinstance(b, Block)

    # x and col not in the same view
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v1,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(facet,v2,f1).
    attribute((facet,channel),f1,col).
    """
        )
        == []
    )

    # x and row in the same view
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(facet,v,f1).
    attribute((facet,channel),f1,row).
    """
        )
        == []
    )

    # x and col in the same view
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(facet,v,f1).
    attribute((facet,channel),f1,col).
    """
    ) == [("x_col", "v")]


def test_y_col():
    b = soft.blocks["y_col"]
    assert isinstance(b, Block)

    # y and col not in the same view
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v1,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(facet,v2,f1).
    attribute((facet,channel),f1,col).
    """
        )
        == []
    )

    # y and row in the same view
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(facet,v,f1).
    attribute((facet,channel),f1,row).
    """
        )
        == []
    )

    # y and col in the same view
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(facet,v,f1).
    attribute((facet,channel),f1,col).
    """
    ) == [("y_col", "v")]


def test_color_entropy_high():
    b = soft.blocks["color_entropy_high"]
    assert isinstance(b, Block)

    # scale on view
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,entropy),precipitation,200).
    attribute((field,interesting),precipitation,true).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,entropy),precipitation,60000).
    attribute((field,interesting),precipitation,true).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
    ) == [("color_entropy_high", "e1")]


def test_color_entropy_low():
    b = soft.blocks["color_entropy_low"]
    assert isinstance(b, Block)

    # scale on view
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,entropy),precipitation,60000).
    attribute((field,interesting),precipitation,true).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,entropy),precipitation,2000).
    attribute((field,interesting),precipitation,true).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
    ) == [("color_entropy_low", "e1")]


def test_size_entropy_high():
    b = soft.blocks["size_entropy_high"]
    assert isinstance(b, Block)

    # scale on view
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,entropy),precipitation,3000).
    attribute((field,interesting),precipitation,true).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,entropy),precipitation,4000).
    attribute((field,interesting),precipitation,true).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).

    entity(scale,root,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
    ) == [("size_entropy_high", "e1")]


def test_size_entropy_low():
    b = soft.blocks["size_entropy_low"]
    assert isinstance(b, Block)

    # scale on view
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,entropy),precipitation,60000).
    attribute((field,interesting),precipitation,true).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,entropy),precipitation,2000).
    attribute((field,interesting),precipitation,true).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).

    entity(scale,root,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
    ) == [("size_entropy_low", "e1")]


def test_linear_scale():
    b = soft.blocks["linear_scale"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("linear_scale", "e1")]

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,linear).
    """
    ) == [("linear_scale", "e1"), ("linear_scale", "e2")]


def test_log_scale():
    b = soft.blocks["log_scale"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,log).
    """
    ) == [("log_scale", "e1")]

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,log).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,log).
    """
    ) == [("log_scale", "e1"), ("log_scale", "e2")]


def test_ordinal_scale():
    b = soft.blocks["ordinal_scale"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("ordinal_scale", "e1")]

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,ordinal).
    """
    ) == [("ordinal_scale", "e1"), ("ordinal_scale", "e2")]


def test_categorical_scale():
    b = soft.blocks["categorical_scale"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
    ) == [("categorical_scale", "e1")]


def test_c_c_point():
    b = soft.blocks["c_c_point"]
    assert isinstance(b, Block)

    # only x encoding, continuous x
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # continuous x, discrete y
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
        )
        == []
    )

    # continuous x, y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,log).
    """
    ) == [("c_c_point", "m1")]


def test_c_c_line():
    b = soft.blocks["c_c_line"]
    assert isinstance(b, Block)

    # continuous x, y, point mark
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # continuous x, y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,line).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,log).
    """
    ) == [("c_c_line", "m1")]


def test_c_c_area():
    b = soft.blocks["c_c_area"]
    assert isinstance(b, Block)

    # continuous y, discrete x
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,area).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,20).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # continuous x, y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,area).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,log).
    """
    ) == [("c_c_area", "m1")]


def test_c_c_text():
    b = soft.blocks["c_c_text"]
    assert isinstance(b, Block)

    # discrete x, y
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,text).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,20).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # continuous x, y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,text).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,linear).
    """
    ) == [("c_c_text", "m1")]


def test_c_d_overlap_point():
    b = soft.blocks["c_d_overlap_point"]
    assert isinstance(b, Block)

    # only x encoding, discrete x
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    """
        )
        == []
    )

    # only x encoding, continuous x
    assert list_preferences(
        b.program
        + """
    attribute(number_rows,root,10).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,2).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,wind).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("c_d_overlap_point", "m1")]

    # continuous and aggregated x, discrete y
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,aggregate),e1,mean).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
        )
        == []
    )

    # continuous x, discrete y, data size > discrete size
    assert list_preferences(
        b.program
        + """
    attribute(number_rows,root,100).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,50).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,wind).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
    ) == [("c_d_overlap_point", "m1")]


def test_c_d_overlap_bar():
    b = soft.blocks["c_d_overlap_bar"]
    assert isinstance(b, Block)

    # continuous and aggregated y, discrete x
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,bar).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,aggregate),e2,count).
    """
        )
        == []
    )

    # continuous y, discrete x, no overlap
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,bar).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s1,linear).
    """
    ) == [("c_d_overlap_bar", "m1")]

    # continuous y, discrete x, non-positional channel color not aggregated
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,bar).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(encoding,m1,e3).
    attribute((encoding,channel),e3,color).
    """
    ) == [("c_d_overlap_bar", "m1")]


def test_c_d_overlap_line():
    b = soft.blocks["c_d_overlap_line"]
    assert isinstance(b, Block)

    #  discrete x, continuous y, bar mark
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,bar).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    """
        )
        == []
    )

    # continuous y, discrete x
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,line).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    """
    ) == [("c_d_overlap_line", "m1")]


def test_c_d_overlap_area():
    b = soft.blocks["c_d_overlap_area"]
    assert isinstance(b, Block)

    #  discrete x, y
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,area).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
        )
        == []
    )

    # continuous y, discrete x
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,area).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,log).
    """
    ) == [("c_d_overlap_area", "m1")]


def test_c_d_overlap_text():
    b = soft.blocks["c_d_overlap_text"]
    assert isinstance(b, Block)

    #  only y, continuous y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,text).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,log).
    """
    ) == [("c_d_overlap_text", "m1")]

    # continuous y, discrete x
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,text).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,categorical).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,linear).
    """
    ) == [("c_d_overlap_text", "m1")]


def test_c_d_overlap_tick():
    b = soft.blocks["c_d_overlap_tick"]
    assert isinstance(b, Block)

    #  only y, discrete y, data size > discrete size(1)
    assert (
        list_preferences(
            b.program
            + """
    attribute(number_rows,root,100).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,100).

    entity(view,root,v).
    entity(mark,v,m1).
    attribute((mark,type),m1,tick).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    helper((encoding,field),e1,wind).

    entity(scale,root,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # continuous x, discrete y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,tick).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,ordinal).
    """
    ) == [("c_d_overlap_tick", "m1")]


def test_c_d_no_overlap_point():
    b = soft.blocks["c_d_no_overlap_point"]
    assert isinstance(b, Block)

    # continuous x, discrete y, data size > discrete size
    assert (
        list_preferences(
            b.program
            + """
    attribute(number_rows,root,100).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,50).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,wind).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
        )
        == []
    )

    # continuous x, discrete y, data size == discrete size
    assert list_preferences(
        b.program
        + """
    attribute(number_rows,root,10).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,10).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,wind).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
    ) == [("c_d_no_overlap_point", "m1")]

    # continuous x, discrete y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).

    helper(no_overlap,m1).
    """
    ) == [("c_d_no_overlap_point", "m1")]


def test_c_d_no_overlap_bar():
    b = soft.blocks["c_d_no_overlap_bar"]
    assert isinstance(b, Block)

    # continuous y, discrete x, no overlap
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,bar).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # continuous y, discrete x, stacked
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,bar).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,stack),e2,zero).
    """
    ) == [("c_d_no_overlap_bar", "m1")]


def test_c_d_no_overlap_tick():
    b = soft.blocks["c_d_no_overlap_tick"]
    assert isinstance(b, Block)

    # continuous aggregated y, discrete x, no overlap
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,tick).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,aggregate),e2,count).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s1,linear).
    """
    ) == [("c_d_no_overlap_tick", "m1")]


def test_d_d_overlap():
    b = soft.blocks["d_d_overlap"]
    assert isinstance(b, Block)

    # discrete x, y; number_rows == D*D
    assert (
        list_preferences(
            b.program
            + """
    attribute(number_rows,root,90).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,100).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
        )
        == []
    )

    # discrete x, y; number_rows > D*D
    assert list_preferences(
        b.program
        + """
    attribute(number_rows,root,1000).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,10).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s1,linear).
    """
    ) == [("d_d_overlap", "m1")]

    # discrete x, y; color channel is aggregated
    assert (
        list_preferences(
            b.program
            + """
    attribute(number_rows,root,100).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,10).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).

    entity(encoding,m1,e3).
    attribute((encoding,channel),e2,color).
    attribute((encoding,aggregate),e3,count).
    """
        )
        == []
    )

    # discrete x, y; number_rows > D*D
    assert list_preferences(
        b.program
        + """
    attribute(number_rows,root,1000).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,10).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).

    entity(encoding,m1,e3).
    attribute((encoding,channel),e2,color).
    """
    ) == [("d_d_overlap", "m1")]

    # only discrete x; number_rows > D
    assert list_preferences(
        b.program
        + """
    attribute(number_rows,root,1000).
    entity(field,root,wind).
    attribute((field,name),wind,wind).
    attribute((field,type),wind,number).
    attribute((field,unique),wind,1000).

    entity(view,root,v).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    helper((encoding,field),e1,wind).
    """
    ) == [("d_d_overlap", "m1")]


def test_d_d_point():
    b = soft.blocks["d_d_point"]
    assert isinstance(b, Block)

    # only x encoding, discrete x
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    """
    ) == [("d_d_point", "m1")]

    # discrete x, y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
    ) == [("d_d_point", "m1")]


def test_d_d_text():
    b = soft.blocks["d_d_text"]
    assert isinstance(b, Block)

    # discrete x, y, point mark
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    attribute((mark,type),m1,point).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,binning),e2,10).
    """
        )
        == []
    )

    # discrete x, y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,text).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("d_d_text", "m1")]


def test_d_d_rect():
    b = soft.blocks["d_d_rect"]
    assert isinstance(b, Block)

    # only y encoding, discrete y
    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    attribute((mark,type),m1,rect).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("d_d_rect", "m1")]

    # discrete x, y, one root scale
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    attribute((mark,type),m1,rect).

    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,categorical).

    entity(scale,root,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,ordinal).
    """
    ) == [("d_d_rect", "m1")]


def test_linear_x():
    b = soft.blocks["linear_x"]
    assert isinstance(b, Block)

    # log x
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,log).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("linear_x", "e1")]


def test_linear_y():
    b = soft.blocks["linear_y"]
    assert isinstance(b, Block)

    # linear x
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,root,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,linear).
    """
    ) == [("linear_y", "e1")]


def test_linear_color():
    b = soft.blocks["linear_color"]
    assert isinstance(b, Block)

    # ordinal color
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
    ) == [("linear_color", "e1")]


def test_linear_size():
    b = soft.blocks["linear_size"]
    assert isinstance(b, Block)

    # log size
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,log).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).

    entity(scale,root,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
    ) == [("linear_size", "e1")]


def test_linear_text():
    b = soft.blocks["linear_text"]
    assert isinstance(b, Block)

    # log text
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    entity(scale,v,s1).
    attribute((scale,channel),s1,text).
    attribute((scale,type),s1,log).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    entity(scale,root,s1).
    attribute((scale,channel),s1,text).
    attribute((scale,type),s1,linear).
    """
    ) == [("linear_text", "e1")]


def test_log_x():
    b = soft.blocks["log_x"]
    assert isinstance(b, Block)

    # linear x
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,log).
    """
    ) == [("log_x", "e1")]


def test_log_y():
    b = soft.blocks["log_y"]
    assert isinstance(b, Block)

    # ordinal y
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,root,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,log).
    """
    ) == [("log_y", "e1")]


def test_log_color():
    b = soft.blocks["log_color"]
    assert isinstance(b, Block)

    # linear color
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,log).
    """
    ) == [("log_color", "e1")]


def test_log_size():
    b = soft.blocks["log_size"]
    assert isinstance(b, Block)

    # log color
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,log).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).

    entity(scale,root,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,log).
    """
    ) == [("log_size", "e1")]


def test_log_text():
    b = soft.blocks["log_text"]
    assert isinstance(b, Block)

    # ordinal text
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    entity(scale,v,s1).
    attribute((scale,channel),s1,text).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # scale on root
    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    entity(scale,root,s1).
    attribute((scale,channel),s1,text).
    attribute((scale,type),s1,log).
    """
    ) == [("log_text", "e1")]


def test_ordinal_x():
    b = soft.blocks["ordinal_x"]
    assert isinstance(b, Block)

    # scale on root, linear x
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("ordinal_x", "e1")]


def test_ordinal_y():
    b = soft.blocks["ordinal_y"]
    assert isinstance(b, Block)

    # scale on root, log y
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,root,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,log).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("ordinal_y", "e1")]


def test_ordinal_color():
    b = soft.blocks["ordinal_color"]
    assert isinstance(b, Block)

    # scale on root, linear color
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("ordinal_color", "e1")]


def test_ordinal_size():
    b = soft.blocks["ordinal_size"]
    assert isinstance(b, Block)

    # scale on root, ordinal color
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("ordinal_size", "e1")]


def test_ordinal_shape():
    b = soft.blocks["ordinal_shape"]
    assert isinstance(b, Block)

    # scale on root, ordinal size
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).

    entity(scale,root,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,shape).

    entity(scale,v,s1).
    attribute((scale,channel),s1,shape).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("ordinal_shape", "e1")]


def test_ordinal_text():
    b = soft.blocks["ordinal_text"]
    assert isinstance(b, Block)

    # scale on root, linear text
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    entity(scale,root,s1).
    attribute((scale,channel),s1,text).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    entity(scale,v,s1).
    attribute((scale,channel),s1,text).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("ordinal_text", "e1")]


def test_ordinal_detail():
    b = soft.blocks["ordinal_detail"]
    assert isinstance(b, Block)

    # scale on root, ordinal x
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,detail).

    entity(scale,v,s1).
    attribute((scale,channel),s1,detail).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("ordinal_detail", "e1")]


def test_categorical_color():
    b = soft.blocks["categorical_color"]
    assert isinstance(b, Block)

    # scale on root, linear color
    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
    ) == [("categorical_color", "e1")]


def test_aggregate_count():
    b = soft.blocks["aggregate_count"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,count).
    """
    ) == [("aggregate_count", "e1")]


def test_aggregate_mean():
    b = soft.blocks["aggregate_mean"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,count).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,mean).
    """
    ) == [("aggregate_mean", "e1")]


def test_aggregate_median():
    b = soft.blocks["aggregate_median"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,min).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,median).
    """
    ) == [("aggregate_median", "e1")]


def test_aggregate_min():
    b = soft.blocks["aggregate_min"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,max).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,min).
    """
    ) == [("aggregate_min", "e1")]


def test_aggregate_max():
    b = soft.blocks["aggregate_max"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,min).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,max).
    """
    ) == [("aggregate_max", "e1")]


def test_aggregate_stdev():
    b = soft.blocks["aggregate_stdev"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,mean).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,stdev).
    """
    ) == [("aggregate_stdev", "e1")]


def test_aggregate_sum():
    b = soft.blocks["aggregate_sum"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,count).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,sum).
    """
    ) == [("aggregate_sum", "e1")]


def test_stack_zero():
    b = soft.blocks["stack_zero"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,count).
    attribute((encoding,stack),e1,zero).
    """
    ) == [("stack_zero", "e1")]


def test_stack_center():
    b = soft.blocks["stack_center"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,count).
    attribute((encoding,stack),e1,zero).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,count).
    attribute((encoding,stack),e1,center).
    """
    ) == [("stack_center", "e1")]


def test_stack_normalize():
    b = soft.blocks["stack_normalize"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,count).
    attribute((encoding,stack),e1,center).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    attribute((encoding,aggregate),e1,count).
    attribute((encoding,stack),e1,normalize).
    """
    ) == [("stack_normalize", "e1")]


def test_value_point():
    b = soft.blocks["value_point"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,line).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).
    """
    ) == [("value_point", "m1")]


def test_value_bar():
    b = soft.blocks["value_bar"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,bar).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,bar).

    entity(mark,v,m2).
    attribute((mark,type),m2,bar).
    """
    ) == [("value_bar", "m1"), ("value_bar", "m2")]


def test_value_line():
    b = soft.blocks["value_line"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,line).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,line).
    """
    ) == [("value_line", "m1")]


def test_value_area():
    b = soft.blocks["value_area"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,bar).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,area).
    """
    ) == [("value_area", "m1")]


def test_value_text():
    b = soft.blocks["value_text"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,tick).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,text).
    """
    ) == [("value_text", "m1")]


def test_value_tick():
    b = soft.blocks["value_tick"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,tick).
    """
    ) == [("value_tick", "m1")]


def test_value_rect():
    b = soft.blocks["value_rect"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,area).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,rect).

    entity(mark,v,m2).
    attribute((mark,type),m2,rect).
    """
    ) == [("value_rect", "m1"), ("value_rect", "m2")]


def test_summary_point():
    b = soft.blocks["summary_point"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).
    """
    ) == [("summary_point", "m1")]


def test_summary_bar():
    b = soft.blocks["summary_bar"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    attribute((mark,type),m1,bar).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,bar).

    entity(mark,v,m2).
    attribute((mark,type),m2,bar).
    """
    ) == [("summary_bar", "m1"), ("summary_bar", "m2")]


def test_summary_line():
    b = soft.blocks["summary_line"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,bar).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,line).
    """
    ) == [("summary_line", "m1")]


def test_summary_area():
    b = soft.blocks["summary_area"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,bar).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,area).
    """
    ) == [("summary_area", "m1")]


def test_summary_text():
    b = soft.blocks["summary_text"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,tick).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,text).
    """
    ) == [("summary_text", "m1")]


def test_summary_tick():
    b = soft.blocks["summary_tick"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,point).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,tick).
    """
    ) == [("summary_tick", "m1")]


def test_summary_rect():
    b = soft.blocks["summary_rect"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,area).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    attribute(task,root,summary).

    entity(mark,v,m1).
    attribute((mark,type),m1,rect).

    entity(mark,v,m2).
    attribute((mark,type),m2,rect).
    """
    ) == [("summary_rect", "m1"), ("summary_rect", "m2")]


def test_value_continuous_x():
    b = soft.blocks["value_continuous_x"]
    assert isinstance(b, Block)

    # discrete x
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    helper((encoding,field),e1,precipitation).
    """
        )
        == []
    )

    # continuous x
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,precipitation).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("value_continuous_x", "e1")]


def test_value_continuous_y():
    b = soft.blocks["value_continuous_y"]
    assert isinstance(b, Block)

    # discrete y
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,y).
    attribute((encoding,binning),e1,10).
    """
        )
        == []
    )

    # continuous y
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    helper((encoding,field),e1,precipitation).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,log).
    """
    ) == [("value_continuous_y", "e1")]


def test_value_continuous_color():
    b = soft.blocks["value_continuous_color"]
    assert isinstance(b, Block)

    # discrete color, scale on root
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).
    helper((encoding,field),e1,precipitation).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    # continuous color
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).
    helper((encoding,field),e1,precipitation).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
    ) == [("value_continuous_color", "e1")]


def test_value_continuous_size():
    b = soft.blocks["value_continuous_size"]
    assert isinstance(b, Block)

    # discrete size
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,binning),e1,10).
    """
        )
        == []
    )

    # continuous size
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
    ) == [("value_continuous_size", "e1")]


def test_value_continuous_text():
    b = soft.blocks["value_continuous_text"]
    assert isinstance(b, Block)

    # continuous text, summary task
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,text).
    """
        )
        == []
    )

    # continuous text
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,text).

    entity(scale,v,s1).
    attribute((scale,channel),s1,text).
    attribute((scale,type),s1,linear).
    """
    ) == [("value_continuous_text", "e1")]


def test_value_discrete_x():
    b = soft.blocks["value_discrete_x"]
    assert isinstance(b, Block)

    # continuous x
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,x).
    """
        )
        == []
    )

    # discrete x
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,binning),e1,20).
    """
    ) == [("value_discrete_x", "e1")]


def test_value_discrete_y():
    b = soft.blocks["value_discrete_y"]
    assert isinstance(b, Block)

    # continuous y
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,y).
    """
        )
        == []
    )

    # discrete y
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,binning),e1,20).
    """
    ) == [("value_discrete_y", "e1")]


def test_value_discrete_color():
    b = soft.blocks["value_discrete_color"]
    assert isinstance(b, Block)

    # discrete color, summary task
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    # discrete color, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("value_discrete_color", "e1")]


def test_value_discrete_size():
    b = soft.blocks["value_discrete_size"]
    assert isinstance(b, Block)

    # continuous size
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # discrete color, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).
    helper((encoding,field),e1,precipitation).

    entity(scale,root,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("value_discrete_size", "e1")]


def test_value_discrete_shape():
    b = soft.blocks["value_discrete_shape"]
    assert isinstance(b, Block)

    # discrete shape, summary task
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,shape).

    entity(scale,v,s1).
    attribute((scale,channel),s1,shape).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # discrete shape, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,shape).

    entity(scale,root,s1).
    attribute((scale,channel),s1,shape).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("value_discrete_shape", "e1")]


def test_value_discrete_text():
    b = soft.blocks["value_discrete_text"]
    assert isinstance(b, Block)

    # continuous text
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,text).
    """
        )
        == []
    )

    # discrete text
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,binning),e1,10).
    """
    ) == [("value_discrete_text", "e1")]


def test_value_discrete_detail():
    b = soft.blocks["value_discrete_detail"]
    assert isinstance(b, Block)

    # discrete detail, summary task
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,detail).
    helper((encoding,field),e1,precipitation).

    entity(scale,v,s1).
    attribute((scale,channel),s1,detail).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # discrete detail, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(view,root,v).
    entity(mark,v,m1).
    helper((encoding,field),e1,precipitation).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,detail).

    entity(scale,root,s1).
    attribute((scale,channel),s1,detail).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("value_discrete_detail", "e1")]


def test_summary_continuous_x():
    b = soft.blocks["summary_continuous_x"]
    assert isinstance(b, Block)

    # discrete x
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,binning),e1,10).
    """
        )
        == []
    )

    # continuous x
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,precipitation).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
    ) == [("summary_continuous_x", "e1")]


def test_summary_continuous_y():
    b = soft.blocks["summary_continuous_y"]
    assert isinstance(b, Block)

    # discrete y
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,y).
    attribute((encoding,binning),e1,10).
    """
        )
        == []
    )

    # continuous y
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,y).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,log).
    """
    ) == [("summary_continuous_y", "e1")]


def test_summary_continuous_color():
    b = soft.blocks["summary_continuous_color"]
    assert isinstance(b, Block)

    # discrete color, scale on root
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).
    helper((encoding,field),e1,precipitation).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    # continuous color
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    helper((encoding,field),e1,precipitation).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,linear).
    """
    ) == [("summary_continuous_color", "e1")]


def test_summary_continuous_size():
    b = soft.blocks["summary_continuous_size"]
    assert isinstance(b, Block)

    # discrete size
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).
    attribute((encoding,binning),e1,10).
    """
        )
        == []
    )

    # continuous size
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
    ) == [("summary_continuous_size", "e1")]


def test_summary_continuous_text():
    b = soft.blocks["summary_continuous_text"]
    assert isinstance(b, Block)

    # continuous text, value task
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,text).
    """
        )
        == []
    )

    # continuous text
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,text).

    entity(scale,v,s1).
    attribute((scale,channel),s1,text).
    attribute((scale,type),s1,linear).
    """
    ) == [("summary_continuous_text", "e1")]


def test_summary_discrete_x():
    b = soft.blocks["summary_discrete_x"]
    assert isinstance(b, Block)

    # continuous x
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,x).
    """
        )
        == []
    )

    # discrete x
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,binning),e1,20).
    """
    ) == [("summary_discrete_x", "e1")]


def test_summary_discrete_y():
    b = soft.blocks["summary_discrete_y"]
    assert isinstance(b, Block)

    # continuous y
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,y).
    """
        )
        == []
    )

    # discrete y
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,binning),e1,20).
    """
    ) == [("summary_discrete_y", "e1")]


def test_summary_discrete_color():
    b = soft.blocks["summary_discrete_color"]
    assert isinstance(b, Block)

    # discrete color, value task
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    # discrete color, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,color).

    entity(scale,root,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("summary_discrete_color", "e1")]


def test_summary_discrete_size():
    b = soft.blocks["summary_discrete_size"]
    assert isinstance(b, Block)

    # continuous size
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,size).
    helper((encoding,field),e1,precipitation).

    entity(scale,v,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # discrete color, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,size).

    entity(scale,root,s1).
    attribute((scale,channel),s1,size).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("summary_discrete_size", "e1")]


def test_summary_discrete_shape():
    b = soft.blocks["summary_discrete_shape"]
    assert isinstance(b, Block)

    # discrete shape, value task
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,shape).

    entity(scale,v,s1).
    attribute((scale,channel),s1,shape).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # discrete shape, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,shape).

    entity(scale,root,s1).
    attribute((scale,channel),s1,shape).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("summary_discrete_shape", "e1")]


def test_summary_discrete_text():
    b = soft.blocks["summary_discrete_text"]
    assert isinstance(b, Block)

    # continuous text
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,text).
    """
        )
        == []
    )

    # discrete text
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,binning),e1,10).
    """
    ) == [("summary_discrete_text", "e1")]


def test_summary_discrete_detail():
    b = soft.blocks["summary_discrete_detail"]
    assert isinstance(b, Block)

    # discrete detail, value task
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,detail).

    entity(scale,v,s1).
    attribute((scale,channel),s1,detail).
    attribute((scale,type),s1,ordinal).
    """
        )
        == []
    )

    # discrete detail, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,detail).

    entity(scale,root,s1).
    attribute((scale,channel),s1,detail).
    attribute((scale,type),s1,ordinal).
    """
    ) == [("summary_discrete_detail", "e1")]


def test_interesting_x():
    b = soft.blocks["interesting_x"]
    assert isinstance(b, Block)

    # discrete detail, value task
    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,x).
    """
        )
        == []
    )

    # discrete detail, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),precipitation,true).
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    helper((encoding,field),e1,precipitation).
    attribute((encoding,channel),e1,x).
    """
    ) == [("interesting_x", "e1")]


def test_interesting_column():
    b = soft.blocks["interesting_column"]
    assert isinstance(b, Block)

    # discrete detail, value task
    assert (
        list_preferences(
            b.program
            + """
    attribute(task,root,value).

    entity(mark,v,m1).
    entity(facet,v,f).
    attribute((facet,field),f,precipitation).
    attribute((facet,channel),f,col).
    """
        )
        == []
    )

    # discrete detail, scale on root
    assert list_preferences(
        b.program
        + """
    attribute((field,interesting),fd,true).
    attribute((field,name),fd,precipitation).
    attribute(task,root,summary).

    entity(view,root,v).
    entity(mark,v,m1).

    entity(facet,v,f).
    attribute((facet,field),f,precipitation).
    attribute((facet,channel),f,col).
    """
    ) == [("interesting_column", "f")]


def test_cartesian_coordinate():
    b = soft.blocks["cartesian_coordinate"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    attribute((view,coordinates),v,polar).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    attribute((view,coordinates),v,cartesian).
    """
    ) == [("cartesian_coordinate", "v")]

    assert list_preferences(
        b.program
        + """
    entity(view,root,v1).
    attribute((view,coordinates),v1,cartesian).
    entity(view,root,v2).
    attribute((view,coordinates),v2,cartesian).
    """
    ) == [("cartesian_coordinate", "v1"), ("cartesian_coordinate", "v2")]


def test_polar_coordinate():
    b = soft.blocks["polar_coordinate"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(view,root,v).
    attribute((view,coordinates),v,cartesian).
    """
        )
        == []
    )

    assert list_preferences(
        b.program
        + """
    entity(view,root,v).
    attribute((view,coordinates),v,polar).
    """
    ) == [("polar_coordinate", "v")]

    assert list_preferences(
        b.program
        + """
    entity(view,root,v1).
    attribute((view,coordinates),v1,polar).
    entity(view,root,v2).
    attribute((view,coordinates),v2,polar).
    """
    ) == [("polar_coordinate", "v1"), ("polar_coordinate", "v2")]
