from draco import is_satisfiable, dict_to_facts
from draco.asp_utils import Block
from draco.programs import hard, helpers


def test_text_mark_without_text_channel():
    b = hard.blocks["text_mark_without_text_channel"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,text).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,channel),e3,text).

    :- violation(_).
    """
    )


def test_text_channel_without_text_mark():
    b = hard.blocks["text_channel_without_text_mark"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,bar).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )


def test_bin_and_aggregate():
    b = hard.blocks["bin_and_aggregate"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    entity(encoding,root,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,aggregate),e2,count).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    attribute((encoding,aggregate),e1,count).

    :- violation(_).
    """
    )


def test_no_encodings():
    b = hard.blocks["no_encodings"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(mark,root,1).
    entity(encoding,1,2).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(mark,root,3).

    :- violation(_).
    """
    )


def test_repeat_channel():
    b = hard.blocks["repeat_channel"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,y).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(scale,root,3).
    attribute((scale,channel),3,x).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(encoding,1,3).
    attribute((encoding,channel),3,y).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).

    :- violation(_).
    """
    )


def test_encoding_no_field_and_not_count():
    b = hard.blocks["encoding_no_field_and_not_count"]
    assert isinstance(b, Block)
    p = b.program
    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,field),1,temp).
    attribute((encoding,aggregate),1,mean).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,mean).

    :- violation(_).
    """
    )


def test_count_with_field():
    b = hard.blocks["count_with_field"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((encoding,aggregate),1,count).
    attribute((encoding,field),1,temp).

    :- violation(_).
    """
    )


def test_point_tick_bar_without_x_or_y():
    b = hard.blocks["point_tick_bar_without_x_or_y"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,color).

    :- violation(_).
    """
    )


def test_enc_type_valid():
    b = hard.blocks["enc_type_valid"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(mark,root,1).
    entity(encoding,1,3).
    entity(scale,root,5).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((field,name),0,temperature).
    attribute((field,type),0,string).
    entity(mark,0,1).
    entity(encoding,1,3).
    entity(scale,0,5).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((field,name),0,temperature).
    attribute((field,type),0,string).
    entity(view,0,1).
    entity(mark,1,2).
    entity(encoding,2,3).
    entity(scale,0,5).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).

    :- violation(_).
    """
    )


def test_bin_q_o():
    b = hard.blocks["bin_q_o"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(view,0,1).
    entity(mark,1,2).
    entity(encoding,2,3).
    entity(scale,0,4).
    attribute((encoding,channel),3,x).
    attribute((encoding,binning),3,10).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )


def test_log_non_positive():
    b = hard.blocks["log_non_positive"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,log).

    :- violation(_).
    """
    )


def test_aggregate_o_valid():
    b = hard.blocks["aggregate_o_valid"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,min).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,median).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,mean).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(view,0,1).
    entity(mark,1,2).
    entity(encoding,2,3).
    entity(scale,0,4).
    attribute((encoding,channel),3,x).
    attribute((encoding,aggregate),3,mean).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).

    :- violation(_).
    """
    )


def test_aggregate_t_valid():
    b = hard.blocks["aggregate_t_valid"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    attribute((field,name),0,time).
    attribute((field,type),0,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,min).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    attribute((field,name),0,time).
    attribute((field,type),0,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,max).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((field,name),0,time).
    attribute((field,type),0,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,median).

    :- violation(_).
    """
    )


def test_aggregate_nominal():
    b = hard.blocks["aggregate_nominal"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,min).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,min).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(view,0,1).
    entity(mark,1,2).
    entity(encoding,2,3).
    entity(scale,0,4).
    attribute((encoding,channel),3,x).
    attribute((encoding,aggregate),3,min).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )


def test_aggregate_detail():
    b = hard.blocks["aggregate_detail"]
    assert isinstance(b, Block)
    p = b.program

    assert not is_satisfiable(
        p
        + """
    attribute((encoding,channel),2,detail).
    attribute((encoding,aggregate),2,min).

    :- violation(_).
    """
    )


def test_count_q_without_field():
    b = hard.blocks["count_q_without_field"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).
    attribute((scale,channel),4,y).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,field),2,temp).
    attribute((encoding,aggregate),2,count).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )


def test_shape_discrete_non_ordered():
    b = hard.blocks["shape_discrete_non_ordered"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    attribute((scale,channel),4,shape).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((scale,channel),4,shape).
    attribute((scale,type),4,ordinal).

    :- violation(_).
    """
    )


def test_detail_non_ordered():
    b = hard.blocks["detail_non_ordered"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    attribute((scale,channel),4,detail).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((scale,channel),4,detail).
    attribute((scale,type),4,ordinal).

    :- violation(_).
    """
    )


def test_size_nominal():
    b = hard.blocks["size_nominal"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    attribute((scale,channel),4,size).
    attribute((scale,type),4,linear).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((scale,channel),4,size).
    attribute((scale,type),4,categorical).

    :- violation(_).
    """
    )


def test_size_negative():
    b = hard.blocks["size_negative"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    attribute((field,min),precipitation,0).
    attribute((field,max),precipitation,55).
    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    attribute((encoding,field),1,precipitation).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).
    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    attribute((encoding,field),1,precipitation).
    :- violation(_).
    """
    )


def test_line_area_without_x_y():
    b = hard.blocks["line_area_without_x_y"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(mark,root,1).
    attribute((mark,type),1,line).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(encoding,1,3).
    attribute((encoding,channel),3,y).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).
    attribute((mark,type),1,line).
    entity(encoding,1,2).
    attribute((encoding,channel),2,y).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).
    attribute((mark,type),1,area).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).
    attribute((mark,type),1,area).
    entity(encoding,1,2).

    :- violation(_).
    """
    )


def test_line_area_with_discrete():
    b = hard.blocks["line_area_with_discrete"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(scale,0,2).
    entity(scale,0,3).
    attribute((mark,type),1,line).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,linear).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,linear).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(scale,0,2).
    entity(scale,0,3).
    attribute((mark,type),1,line).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,categorical).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,linear).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,0,1).
    entity(scale,0,2).
    entity(scale,0,3).
    attribute((mark,type),1,line).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,categorical).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,ordinal).

    :- violation(_).
    """
    )


def test_bar_tick_continuous_x_y():
    b = hard.blocks["bar_tick_continuous_x_y"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(mark,0,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + ("\n").join(
            dict_to_facts(
                {
                    "mark": [
                        {
                            "type": "tick",
                            "encoding": [
                                {"channel": "x", "field": "temperature"},
                                {"channel": "y", "field": "wind"},
                            ],
                        }
                    ],
                    "scale": [
                        {"channel": "x", "type": "linear"},
                        {"channel": "y", "type": "categorical"},
                    ],
                }
            )
        )
        + """
    :- violation(_).
    """
    )

    # multiple views
    assert not is_satisfiable(
        p
        + ("\n").join(
            dict_to_facts(
                {
                    "view": [
                        {
                            "mark": [
                                {
                                    "type": "tick",
                                    "encoding": [
                                        {"channel": "y", "field": "temperature"}
                                    ],
                                }
                            ],
                            "scale": [{"channel": "y", "type": "linear"}],
                        },
                        {
                            "mark": [
                                {
                                    "type": "bar",
                                    "encoding": [
                                        {"channel": "x", "field": "temperature"},
                                        {"channel": "y", "aggregate": "count"},
                                    ],
                                }
                            ],
                            "scale": [
                                {"channel": "x", "type": "linear"},
                                {"channel": "y", "type": "linear"},
                            ],
                        },
                    ]
                }
            )
        )
        + """
    :- violation(_).
    """
    )

    # multiple views with one shared-scale
    assert is_satisfiable(
        p
        + ("\n").join(
            dict_to_facts(
                {
                    "view": [
                        {
                            "mark": [
                                {
                                    "type": "tick",
                                    "encoding": [
                                        {"channel": "y", "field": "temperature"}
                                    ],
                                }
                            ]
                        },
                        {
                            "mark": [
                                {
                                    "type": "bar",
                                    "encoding": [
                                        {"channel": "x", "field": "temperature"},
                                        {"channel": "y", "aggregate": "count"},
                                    ],
                                }
                            ],
                            "scale": [{"channel": "x", "type": "ordinal"}],
                        },
                    ],
                    "scale": [{"channel": "y", "type": "linear"}],
                }
            )
        )
        + """
    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + ("\n").join(
            dict_to_facts(
                {
                    "view": [
                        {
                            "mark": [
                                {
                                    "type": "tick",
                                    "encoding": [
                                        {"channel": "y", "field": "temperature"}
                                    ],
                                }
                            ]
                        },
                        {
                            "mark": [
                                {
                                    "type": "bar",
                                    "encoding": [
                                        {"channel": "x", "field": "temperature"},
                                        {"channel": "y", "aggregate": "count"},
                                    ],
                                }
                            ],
                            "scale": [{"channel": "x", "type": "linear"}],
                        },
                    ],
                    "scale": [{"channel": "y", "type": "linear"}],
                }
            )
        )
        + """
    :- violation(_).
    """
    )
