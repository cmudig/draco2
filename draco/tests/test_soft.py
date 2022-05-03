from draco.asp_utils import Block
from draco.programs import define, helpers, soft
from draco.run import run_clingo


def list_preferences(program: str):
    try:
        model = next(run_clingo(helpers.program + define.program + program, 1))

        return [
            tuple(map(lambda x: x.name, symbol.arguments))
            for symbol in model.answer_set
            if symbol.name == "preference"
        ]
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

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,aggregate),e1,mean).
    """
        )
        == [("aggregate", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,aggregate),e1,mean).
    attribute((encoding,aggregate),e2,mean).
    """
        )
        == [("aggregate", "e1"), ("aggregate", "e2")]
    )


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

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,10).
    """
        )
        == [("bin", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,10).
    attribute((encoding,binning),e2,20).
    """
        )
        == [("bin", "e1"), ("bin", "e2")]
    )


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

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,13).
    """
        )
        == [("bin_high", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,14).
    attribute((encoding,binning),e2,20).
    """
        )
        == [("bin_high", "e1"), ("bin_high", "e2")]
    )


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

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,3).
    """
        )
        == [("bin_low", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,7).
    attribute((encoding,binning),e2,3).
    """
        )
        == [("bin_low", "e1"), ("bin_low", "e2")]
    )


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

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    """
        )
        == [("encoding", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    entity(encoding,m1,e2).
    """
        )
        == [("encoding", "e1"), ("encoding", "e2")]
    )


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

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,field),e1,temperature).
    """
        )
        == [("encoding_field", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,date).
    """
        )
        == [("encoding_field", "e1"), ("encoding_field", "e2")]
    )


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

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,date).
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

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    """
        )
        == [("same_field", "temperature")]
    )

    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).
    entity(field,root,date).

    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).
    entity(encoding,m,e3).
    entity(encoding,m,e4).

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    attribute((encoding,field),e3,date).
    attribute((encoding,field),e4,date).
    """
        )
        == [("same_field", "temperature"), ("same_field", "date")]
    )

    # use field temperature twice with mark m1, and field date with 2 different marks
    assert (
        list_preferences(
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

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    attribute((encoding,field),e3,date).
    attribute((encoding,field),e4,date).
    """
        )
        == [("same_field", "temperature")]
    )


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

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,date).
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

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
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


    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    attribute((encoding,field),e3,temperature).
    """
        )
        == []
    )

    # use field temperature 3 times with the same mark
    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).

    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).
    entity(encoding,m,e3).

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    attribute((encoding,field),e3,temperature).
    """
        )
        == [("same_field_grt3", "temperature")]
    )

    # use field temperature 4 times with the same mark
    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).

    entity(mark,v,m).

    entity(encoding,m,e1).
    entity(encoding,m,e2).
    entity(encoding,m,e3).
    entity(encoding,m,e4).

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    attribute((encoding,field),e3,temperature).
    attribute((encoding,field),e4,temperature).
    """
        )
        == [("same_field_grt3", "temperature")]
    )


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
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    attribute((encoding,aggregate),e1,count).
    attribute((encoding,aggregate),e2,count).
    """
        )
        == [("count_grt1", "m")]
    )

    # 3 counts
    assert (
        list_preferences(
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
        )
        == [("count_grt1", "m")]
    )


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
    attribute((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).
    """
        )
        == []
    )

    # root scale, categorical for number
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).

    entity(view,root,v).
    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,root,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,categorical).
    """
        )
        == [("number_categorical", "m", "temperature", "x")]
    )

    # two scales, categorical for number
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).

    entity(mark,v1,m).
    entity(encoding,m,e1).
    attribute((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(scale,v1,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,categorical).

    entity(scale,v2,s2).
    attribute((scale,channel),s2,x).
    attribute((scale,type),s2,linear).
    """
        )
        == [("number_categorical", "m", "temperature", "x")]
    )

    # number field used for two times (in same mark)
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).

    entity(mark,v1,m1).
    entity(encoding,m1,e1).
    attribute((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,x).

    entity(encoding,m1,e2).
    attribute((encoding,field),e2,temperature).
    attribute((encoding,channel),e2,color).

    entity(scale,v1,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v1,s2).
    attribute((scale,channel),s2,color).
    attribute((scale,type),s2,categorical).
    """
        )
        == [("number_categorical", "m1", "temperature", "color")]
    )


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
    attribute((encoding,field),e1,temperature).
    attribute((encoding,binning),e1,20).
    """
        )
        == []
    )

    # datetime
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),date,datetime).
    attribute((field,unique),date,10).
    attribute((encoding,field),e1,date).
    attribute((encoding,binning),e1,5).
    """
        )
        == [("bin_low_unique", "e1")]
    )


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
    attribute((scale,type),s1,log).
    """
        )
        == [("bin_not_linear", "e1")]
    )


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

    # 1 encoding
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
        == [("only_discrete", "m1")]
    )

    # 2 encodings
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
    attribute((scale,type),s1,ordinal).
    """
        )
        == [("only_discrete", "m1")]
    )

    # shared scale
    assert (
        list_preferences(
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
        )
        == [("only_discrete", "m1"), ("only_discrete", "m2")]
    )


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

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,size).
    """
        )
        == [("multi_non_pos", "m1")]
    )


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
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,color).
    """
        )
        == [("non_pos_used_before_pos", "m1")]
    )

    # x is not used yet
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,color).
    """
        )
        == [("non_pos_used_before_pos", "m1")]
    )


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
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,size).
    """
        )
        == [("only_y", "m1")]
    )

    # 2 marks
    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,y).

    entity(mark,v,m2).
    entity(encoding,m2,e2).
    attribute((encoding,channel),e2,x).
    """
        )
        == [("only_y", "m1")]
    )


def test_binned_orientation_not_x():
    b = soft.blocks["binned_orientation_not_x"]
    assert isinstance(b, Block)

    # number
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),temperature,number).
    attribute((encoding,field),e1,temperature).
    attribute((encoding,binning),e1,20).
    attribute((encoding,channel),e1,x).
    """
        )
        == []
    )

    # datetime
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,type),date,datetime).
    attribute((encoding,field),e1,date).
    attribute((encoding,binning),e1,20).
    attribute((encoding,channel),e1,y).
    """
        )
        == [("binned_orientation_not_x", "e1")]
    )


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
    attribute((encoding,field),e1,date).
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
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,1461).

    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == [("high_cardinality_ordinal", "e1")]
    )


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
    attribute((encoding,field),e1,weather).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),weather,15).

    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,field),e1,weather).
    attribute((encoding,channel),e1,color).

    entity(scale,v,s1).
    attribute((scale,channel),s1,color).
    attribute((scale,type),s1,categorical).
    """
        )
        == [("high_cardinality_categorical_grt10", "e1")]
    )


def test_high_cardinality_shape():
    b = soft.blocks["high_cardinality_shape"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,25).
    attribute((encoding,field),e1,date).
    attribute((encoding,channel),e1,shape).
    attribute((encoding,binning),e1,5).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),weather,15).
    attribute((encoding,field),e1,weather).
    attribute((encoding,channel),e1,shape).
    """
        )
        == [("high_cardinality_shape", "e1")]
    )


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
    attribute((encoding,field),e1,date).
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
    attribute((encoding,field),e1,weather).
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
    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),temperature,150).

    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,field),e1,temperature).
    attribute((encoding,channel),e1,y).

    entity(encoding,m,e2).
    attribute((encoding,channel),e2,size).

    entity(scale,v,s1).
    attribute((scale,channel),s1,y).
    attribute((scale,type),s1,linear).
    """
        )
        == [("high_cardinality_size", "e1")]
    )


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
    attribute((encoding,field),e1,date).
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
    attribute((encoding,field),e1,date).
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
    attribute((field,unique),date,1461).

    entity(mark,v,m).
    entity(encoding,m,e1).
    attribute((encoding,field),e1,date).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == [("horizontal_scrolling_x", "e1")]
    )


def test_horizontal_scrolling_col():
    b = soft.blocks["horizontal_scrolling_col"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,1461).

    entity(facet,v,f).
    attribute((facet,field),f,date).
    attribute((facet,channel),f,col).
    attribute((facet,binning),f,5).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((field,unique),date,1461).

    entity(facet,v,f).
    attribute((facet,field),f,date).
    attribute((facet,channel),f,col).
    """
        )
        == [("horizontal_scrolling_col", "f")]
    )


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
        == [("linear_scale", "e1")]
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

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,linear).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,linear).
    """
        )
        == [("linear_scale", "e1"), ("linear_scale", "e2")]
    )


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
        == [("log_scale", "e1")]
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

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,log).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,log).
    """
        )
        == [("log_scale", "e1"), ("log_scale", "e2")]
    )


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

    assert (
        list_preferences(
            b.program
            + """
    entity(mark,v,m1).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).
    """
        )
        == [("ordinal_scale", "e1")]
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

    entity(scale,v,s1).
    attribute((scale,channel),s1,x).
    attribute((scale,type),s1,ordinal).

    entity(scale,v,s2).
    attribute((scale,channel),s2,y).
    attribute((scale,type),s2,ordinal).
    """
        )
        == [("ordinal_scale", "e1"), ("ordinal_scale", "e2")]
    )


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
        == [("categorical_scale", "e1")]
    )
